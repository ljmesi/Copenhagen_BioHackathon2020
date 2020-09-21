#!/usr/bin/env python3

import boto3
import json
import logging
from typing import List, Dict
from werkzeug.exceptions import NotFound
from lib.models import Article, Author, Keyword, File, db
from dateutil.parser import parse
from mysql.connector.errors import IntegrityError
from sqlalchemy.exc import DatabaseError

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
queue_url = 'https://sqs.eu-central-1.amazonaws.com/397254617684/crawler_queue'

# TODO: client should recognize environment
sqs_client = boto3.client('sqs')


def get_messages(max_number: int) -> Dict:
    log.debug("fetching messages")
    return sqs_client.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['All'],
        MaxNumberOfMessages=max_number)


def delete_message(rcpt_handle):
    log.debug("deleting message with handle: " + str(rcpt_handle))
    return sqs_client.delete_message(QueueUrl=queue_url,
                                     ReceiptHandle=rcpt_handle)


def get_or_create(model, **kwargs):
    log.debug("checking kwargs")
    for key, value in kwargs.items():
        if key == "digital_object_id" and value != None:
            instance = db.session.query(model).filter_by(digital_object_id=value).first()
            if instance:
                log.debug("querying using digital_object_id : " + value + " yeilded id: " + str(instance.id))
                return instance
        elif key == "title" and value != None:
            try:
                instance = db.session.query(model).filter_by(title=value).first()
                if instance:
                    log.debug("querying title : " + value + " yeilded id: " + str(instance.id))
                    return instance
            except Exception as e:
                log.error("could not filter for instance title", exc_info=True)
                return None
    try:
        log.debug("attempting to query for all parameters")
        instance = db.session.query(model).filter_by(**kwargs).first()
        if instance:
            log.debug("querying using all parameters yeilded id: " + str(instance.id))
            return instance
    except DatabaseError as e:
        log.info("could not fetch instance")
    else:
        log.info("attempting to create new instance")
        instance = model(**kwargs)
        db.session.add(instance)
        try:
            db.session.commit()
            db.session.refresh(instance)
            log.info("returning instance with id: " + str(instance.id))
            return instance
        except IntegrityError as e:
            log.info("could not commit session", exc_info=True)


def fetch_article(article: Article) -> Article:
    try:
        if Article.digital_object_id != None:
            return db.session.query(Article).filter(
                Article.digital_object_id == article.digital_object_id).first_or_404()
    except NotFound as nf:
        log.debug("article not found by digital object id, trying title")
        if Article.title != None:
            return db.session.query(Article).filter(
                Article.title == article.title).first_or_404()
    except Exception as e:
        log.debug("could not find article")
        return None


def save_obj(obj) -> None:
    log.debug("saving obj: " + str(obj))
    try:
        db.session.add(obj)
    except Exception as e:
        db.session.rollback()
        log.error("could not add object to session: " + str(obj), exc_info=1)
    try:
        db.session.commit()
        db.session.refresh(obj)
        log.debug("object id generated: " + str(obj.id))
    except Exception as e:
        db.session.rollback()
        log.error("could not save obj: " + str(obj), exc_info=1)


# TODO
def create_and_load_authors(authors: List[Dict], article: Article) -> List[Author]:
    author_list = list()
    for author in authors:
        a = Author()
        a.article_id = article.id
        a.author_name = author.get('author_name', "")
        author_list.append(a)
    return author_list


def create_and_load_files(files: List[Dict], article: Article) -> List[File]:
    file_list = list()
    for f_ in files:
        file_name = f_.get('file_name', '')
        file_name = file_name.encode("utf-8")
        log.debug("creating File from file: " + str(f_))
        if article.id:
            result = get_or_create(File, article_id=article.id,
                                   file_name=file_name,
                                   url=f_.get('url', ''),
                                   download_url=f_.get('download_url', ''),
                                   digital_object_id=f_.get('digital_object_id', ''))
            if result:
                file_list.append(result)
    return file_list


def create_and_load_keywords(keywords: List[str]) -> List[Keyword]:
    keyword_list = list()
    for k_ in keywords:
        result = get_or_create(Keyword, word=k_)
        if result:
            keyword_list.append(result)
    return keyword_list


def build_article_from_body(msg_body: Dict) -> Article:
    log.debug("building article from message body: \n")
    doi = msg_body.get('digital_object_id', None)
    if doi == '':
        doi = None
    parse_date = msg_body.get('parse_date', '')
    upload_date = msg_body.get('upload_date', "")
    title = msg_body.get('title', "")
    art = get_or_create(Article,
                        digital_object_id=doi,
                        title=title,
                        source_url=msg_body.get('source_url', ""),
                        description=msg_body.get('description', ""),
                        parse_date=str(parse(parse_date)) if parse_date else None,
                        upload_date=str(parse(upload_date)) if upload_date else None,
                        parent_request_url=msg_body.get('parent_request_url', ""),
                        enriched=msg_body.get('enriched', False),
                        published=msg_body.get('published', False))
    if not art:
        log.debug("failed to create article with title: " + str(title))
        return None
    try:
        art.files = create_and_load_files(msg_body.get('files', []), art)
        art.keywords = create_and_load_keywords(msg_body.get('keywords', []))
    except Exception as e:
        log.debug("could not load files and keywords", exc_info=1)
    log.debug("returning article: " + str(art))
    return art


def create_articles(articles: List[Article]) -> List[int]:
    article_id_list = []
    log.debug("starting post process of articles")
    for article in articles:
        fetch_result = fetch_article(article)
        if fetch_result is None:
            save_obj(article)
        if article is not None and article.id != None:
            log.debug("adding article id" + str(article.id))
            article_id_list.append(article.id)
    return article_id_list


def process_messages() -> List[int]:
    msg_dict = get_messages(10)
    msg_list = msg_dict.get('Messages', [])
    log.debug("current message size: " + str(len(msg_list)))
    article_list = list()
    for msg in msg_list:
        msg_id = msg['MessageId']
        rec_handle = msg['ReceiptHandle']
        body_md5 = msg['MD5OfBody']
        msg_body = json.loads(msg['Body'])
        msg_attributes = msg['Attributes']
        article = build_article_from_body(msg_body)
        if article:
            article_list.append(article)
            delete_message(rec_handle)
    id_list = create_articles(article_list)
    log.info("created articles with ids: " + str(id_list))
    return id_list


if __name__ == '__main__':
    while (len(process_messages()) != 0):
        log.info("processing messages")
    log.info("finished processing messages")
