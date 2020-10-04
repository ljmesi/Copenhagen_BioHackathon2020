#!/usr/bin/env python3
import datetime

from flask import Flask, render_template, request


import logging
from flask.json import jsonify
from lib.secrets import DbCredentials, LocalDbCredentials

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

##TODO: re-create tables as utf-8 encoded
DB_CONNECTION = "mysql+mysqlconnector://{user}:{password}@{server}/{db_name}?charset=utf8"


def get_db_connection():
    db_credentials = None
    try:
        log.info("fetching aws credentials")
        db_credentials = DbCredentials()
    except Exception as e:
        log.info("aws unavailable, trying local")
        db_credentials = LocalDbCredentials("secrets.yaml")
    except AttributeError as ae:
        log.info("unable to load credentials")
    return DB_CONNECTION.format(
            user=db_credentials.username,
            password=db_credentials.password,
            server=db_credentials.host,
            db_name=db_credentials.dbname,
        )

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = get_db_connection()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'

from lib.models import *
from lib.encoder import *

def paginate_articles(page=1, per_page=10):
    article_list = []
    try:
        encoder = ConsumerJSONEncoder()
        ##TODO: handle page, per_page strings better
        items = Article.query.order_by(Article.id.desc()).paginate(int(page), int(per_page)).items
        article_list = [encoder.default(x) for x in items if x]
    except Exception:
        log.info("could not get article list", exc_info=True)
    return article_list

@app.route('/')
def get_root():
    log.info("sending root")
    return render_template('index.html')

@app.route('/swagger')
def get_docs():
    return render_template('swaggerui.html')

@app.route('/articles')
def get_articles():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    log.info("page: " + str(page) + " per_page: " + str(per_page))
    articles = paginate_articles(page, per_page)
    return jsonify(articles)
