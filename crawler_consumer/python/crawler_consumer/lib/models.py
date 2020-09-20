#!/usr/bin/env python3

import logging
import datetime
from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.ext.declarative import declarative_base


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


Model = db.Model
Boolean = db.Boolean
Column = db.Column
Integer = db.Integer
String = db.String
Text = db.Text
TIMESTAMP = db.TIMESTAMP
ForeignKey = db.ForeignKey
Table = db.Table

Base = declarative_base()

keywords = Table(
    "keywords",
    Column("keyword_id", Integer, ForeignKey("keyword.id"), primary_key=True),
    Column("article_id", Integer, ForeignKey("article.id"), primary_key=True),
)

class Article(Model, Base):
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    source_url = Column(Text)
    keywords = db.relationship(
        "Keyword",
        secondary=keywords,
        lazy="subquery",
        passive_deletes=True,
        backref=db.backref("articles", lazy=True),
    )
    files = db.relationship("File", backref="article", lazy=True, passive_deletes=True)
    digital_object_id = Column(String(128), unique=True)
    parent_request_url = Column(String(255))
    description = Column(Text)
    parse_date = Column(TIMESTAMP(timezone=True))
    upload_date = Column(TIMESTAMP(timezone=True))
    created_date = Column(
        TIMESTAMP(timezone=True), default=datetime.datetime.utcnow
    )
    modified_date = Column(
        TIMESTAMP(timezone=True), default=datetime.datetime.utcnow
    )
    parsed = Column(Boolean, unique=False, default=False)
    enriched = Column(Boolean, unique=False, default=False)
    published = Column(Boolean, unique=False, default=False)


    def __repr__(self):
        return "<Article %r %s>" % (self.id, self.title)

class Author(Model, Base):
    id = Column(Integer, primary_key=True)
    author_name = Column(String(255))
    article_id = Column(
        Integer, ForeignKey("article.id", ondelete="CASCADE"), nullable=False)

class Keyword(Model, Base):
    id = Column(Integer, primary_key=True)
    word = Column(String(128), unique=True)
    created_date = Column(
        TIMESTAMP(timezone=True), default=datetime.datetime.utcnow
    )
    modified_date = Column(
        TIMESTAMP(timezone=True), default=datetime.datetime.utcnow
    )

    def __repr__(self):
        return "<Article %r, %s>" % (self.id, self.word)


class File(Model, Base):
    id = Column(Integer, primary_key=True)
    article_id = Column(
        Integer, ForeignKey("article.id", ondelete="CASCADE"), nullable=False
    )
    file_name = Column(String(255))
    url = Column(String(255), unique=True)
    download_url = Column(String(255), unique=True)
    digital_object_id = Column(String(255))
    size = Column(Integer)

    def __repr__(self):
        return "<Article %r %s>" % (self.id, self.file_name)
