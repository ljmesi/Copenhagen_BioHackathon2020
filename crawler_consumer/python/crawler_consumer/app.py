#!/usr/bin/env python3
import datetime

from flask import Flask

import yaml
import logging
from flask.json import JSONEncoder
from crawler_consumer.python.crawler_consumer.secrets import DbCredentials
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

##TODO: re-create tables as utf-8 encoded
DB_CONNECTION = "mysql+mysqlconnector://{user}:{password}@{server}/{db_name}?charset=utf8"


def get_db_connection():
    db_credentials = DbCredentials()
    return DB_CONNECTION.format(
        user=db_credentials.username,
        password=db_credentials.password,
        server=db_credentials.host,
        db_name=db_credentials.dbname,
    )


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = get_db_connection()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# engine = db.create_engine(DB_CONNECTION)
# connection = engine.connect()
# metadata = db.MetaData()

keywords = db.Table(
    "keywords",
    db.Column("keyword_id", db.Integer, db.ForeignKey("keyword.id"), primary_key=True),
    db.Column("article_id", db.Integer, db.ForeignKey("article.id"), primary_key=True),
)

class ConsumerJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Article):
            return {
   "id": obj.id,
   "title": obj.title,
   "source_url": obj.source_url,
   "keywords": [ self.default(x) for x in obj.keywords],
   "files": [ self.default(x) for x in obj.files],
   "digital_object_id": obj.digital_object_id,
   "parent_request_url": obj.parent_request_url,
   "description": obj.description,
   "parse_date": obj.parse_date.isoformat() if obj.parse_date is not None else None,
   "upload_date": obj.upload_date.isoformat() if obj.upload_date is not None else None,
   "created_date": obj.created_date.isoformat() if obj.created_date is not None else None,
   "modified_date": obj.modified_date.isoformat() if obj.modified_date is not None else None,
   "parsed": obj.parsed,
   "enriched": obj.enriched,
   "published": obj.published }
        if isinstance(obj, File):
             return {
                     "id": obj.id,
                     "file_name": obj.file_name,
                     "url": obj.url, 
                     "download_url": obj.download_url,
                     "digital_object_id": obj.digital_object_id,
                     "size": obj.size
                    }
        if isinstance(obj, Keyword):
            return {
                   "id": obj.id,
                   "word": obj.word,
                   "created_date": obj.created_date.isoformat() if obj.created_date is not None else None,
                   "modified_date": obj.modified_date.isoformat() if obj.modified_date is not None else None
                  }


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    source_url = db.Column(db.String(255))
    keywords = db.relationship(
        "Keyword",
        secondary=keywords,
        lazy="subquery",
        passive_deletes=True,
        backref=db.backref("articles", lazy=True),
    )
    files = db.relationship("File", backref="article", lazy=True, passive_deletes=True)
    digital_object_id = db.Column(db.String(128), unique=True)
    parent_request_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    parse_date = db.Column(db.TIMESTAMP(timezone=True))
    upload_date = db.Column(db.TIMESTAMP(timezone=True))
    created_date = db.Column(
        db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow
    )
    modified_date = db.Column(
        db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow
    )
    parsed = db.Column(db.Boolean, unique=False, default=False)
    enriched = db.Column(db.Boolean, unique=False, default=False)
    published = db.Column(db.Boolean, unique=False, default=False)


    def __repr__(self):
        return "<Article %r %s>" % (self.id, self.title)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(255))
    article_id = db.Column(
        db.Integer, db.ForeignKey("article.id", ondelete="CASCADE"), nullable=False)

class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(128), unique=True)
    created_date = db.Column(
        db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow
    )
    modified_date = db.Column(
        db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow
    )

    def __repr__(self):
        return "<Article %r, %s>" % (self.id, self.word)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(
        db.Integer, db.ForeignKey("article.id", ondelete="CASCADE"), nullable=False
    )
    file_name = db.Column(db.String(255))
    url = db.Column(db.String(255), unique=True)
    download_url = db.Column(db.String(255), unique=True)
    digital_object_id = db.Column(db.String(255))
    size = db.Column(db.Integer)

    def __repr__(self):
        return "<Article %r %s>" % (self.id, self.file_name)
