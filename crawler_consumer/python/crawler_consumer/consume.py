#!/usr/bin/env python3

import boto3
import json
import logging
from typing import List, Dict
from app import Article, Author, Keyword, File, db, ConsumerJSONEncoder

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
queue_url = 'https://sqs.eu-central-1.amazonaws.com/397254617684/crawler_queue'

sqs_client = boto3.client('sqs')


def get_messages(max_number:int) -> Dict:
    return sqs_client.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['All'],
        MaxNumberOfMessages=max_number)

def fetch_article(article:Article)->Article:
    try:
        return db.session.query(Article).filter(Article.digital_object_id == article.digital_object_id).first()
    except Exception as e:
        log.info("could not use doi from article, using title")
        return db.session.query(Article).filter(Article.title == article.title).first()

def keyword_exists(word:str):
    word_encoded = word.encode(encoding="utf-8").decode("utf-8")
    return True if db.session.query(Keyword.id).filter_by(word=word_encoded).scalar() is not None else False

def file_exists(url:str):
    return True if db.session.query(File.id).filter_by(url=url).scalar() is not None else False

def article_exists(article:Article):
    try:
        return True if db.session.query(Article.id).filter_by(digital_object_id=article.digital_object_id).scalar() is not None else False
    except Exception as e:
        log.info("could not find doi for article, using title for query")
        return True if db.session.query(Article.id).filter_by(title=article.title).scalar() is not None else False


def save_obj(obj)->None:
    log.info("saving obj: " + str(obj))
    try:
        db.session.add(obj)
    except Exception as e:
        db.session.rollback()
        log.error("could not add object to session: " + str(obj), exc_info=1)
    try:
        db.session.commit()
        db.session.refresh(obj)
        log.info("object id generated: " + str(obj.id))
    except Exception as e:
        db.session.rollback()
        log.error("could not save obj: " + str(obj), exc_info=1)

    #TODO
def create_and_load_authors(authors:List[Dict], article:Article)->List[Author]:
    author_list = list()
    for author in authors:
        a = Author()
        a.article_id = article.id
        a.author_name = author.get('author_name', "")
        author_list.append(a)
    return author_list

def create_and_load_files(files:List[Dict], article:Article) -> List[File]:
    file_list = list()
    for f_ in files:
        log.info("creating File from file: " + str(f_))
        if not file_exists(f_.get('url')):
            f = File()
            f.article_id = article.id
            f.file_name = f_.get('file_name', "")
            f.url = f_.get('url', "")
            f.download_url = f_.get('download_url', "")
            f.digital_object_id = f_.get('digital_object_id', "")
            save_obj(f)
            file_list.append(f)
        else:
            result = db.session.query(File).filter(File.file_name == f_['file_name'])
            if result is not None:
                file_obj = result.first()
                if file_obj not in file_list:
                    file_list.append(file_obj)
    return file_list

def create_and_load_keywords(keywords:List[str])->List[Keyword]:
    keyword_list = list()
    for k_ in keywords:
        if not keyword_exists(k_):
            k = Keyword()
            k.word = k_
            save_obj(k)
            keyword_list.append(k)
        else:
            result = db.session.query(Keyword).filter(Keyword.word == k_)
            if result is not None:
                kword = result.first()
                if kword not in keyword_list:
                    keyword_list.append(kword)
    return keyword_list

def build_article_from_body(msg_body:Dict) -> Article:
    doi = msg_body.get('digital_object_id', "")
    art = Article()
    log.info("building article from message body" + str(msg_body))
    art.title = msg_body.get('title', "")
    art.source_url = msg_body.get('source_url', "")
    art.digital_object_id = doi if doi != '' else None
    art.description = msg_body.get('description', "")
    art.parse_date = msg_body.get('parse_date', "")
    art.upload_date = msg_body.get('upload_date', "")
    art.parent_request_url = msg_body.get('parent_request_url', "")
    art.enriched = msg_body.get('enriched', "")
    art.published = msg_body.get('published', "")
    if article_exists(art):
        existing_article = fetch_article(art)
        existing_article.title = existing_article.title if not existing_article.title is None else art.title
        existing_article.source_url = existing_article.source_url if not existing_article.source_url is None else art.source_url
        existing_article.description = existing_article.description if not existing_article.description is None else art.description
        existing_article.parse_date = existing_article.parse_date if not existing_article.parse_date is None else art.parse_date
        existing_article.upload_date = existing_article.upload_date if not existing_article.upload_date is None else art.upload_date
        existing_article.parent_request_url = existing_article.parent_request_url if not existing_article.parent_request_url is None else art.parent_request_url
        existing_article.enriched = existing_article.enriched if not existing_article.enriched is None else art.enriched
        existing_article.published = existing_article.published if not existing_article.published is None else art.published
        save_obj(existing_article)
        art = existing_article

    else:
        if art.digital_object_id == '':
            art.digital_object_id == None
        save_obj(art)
    art.files = create_and_load_files(msg_body.get('files', []), art)
    art.keywords = create_and_load_keywords(msg_body.get('keywords', []))
    try:
        encoder = ConsumerJSONEncoder()
        print(json.dumps(encoder.default(art), indent=4))
    except Exception as e:
        log.info("could not encode object", exc_info=1)
    return art

def create_articles(articles:List[Article])->List[int]:
    article_id_list = []
    for article in articles:
        if not article_exists(article):
            log.info("saving article: ", article.title)
            if article.digital_object_id == '':
                article.digital_object_id == None
            save_obj(article)
        else:
            result = fetch_article(article)
            if result is not None:
                article_obj = result
                if article_obj.id not in article_id_list:
                    article_id_list.append(article_obj.id)
    return article_id_list


if __name__ == '__main__':
    article_list = []
    msg_dict = get_messages(1)
    for msg in msg_dict.get('Messages', []):
        msg_id = msg['MessageId']
        rec_handle = msg['ReceiptHandle']
        body_md5 = msg['MD5OfBody']
        msg_body = json.loads(msg['Body'])
        msg_attributes = msg['Attributes']
        article = build_article_from_body(msg_body)
        article_list.append(article)
    id_list = create_articles(article_list)
    print("created articles with ids: " + str(id_list))
