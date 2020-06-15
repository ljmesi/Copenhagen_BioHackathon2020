#!/usr/bin/env python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import datetime

DB_CONNECTION = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
#user=<USERNAME>, password=<PASSWORD>, server=<SERVER>, database='mdcrawler_consumer'
user='sgarcia', password='Astros123', server='localhost', database='mdcrawler_consumer'
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =DB_CONNECTION

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#engine = db.create_engine(DB_CONNECTION)
#connection = engine.connect()
#metadata = db.MetaData()

keywords = db.Table('keywords',
    db.Column('keyword_id', db.Integer, db.ForeignKey('keyword.id'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True)
)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    source_url = db.Column(db.String(255))
    keywords = db.relationship('Keyword', secondary=keywords, lazy='subquery',
        backref=db.backref('articles', lazy=True))
    files = db.relationship('File', backref='article', lazy=True)
    digital_object_id = db.Column(db.String(128))
    parent_request_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    parse_date = db.Column(db.TIMESTAMP(timezone=True))
    created_date = db.Column(db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    modified_date = db.Column(db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Article %r %s>' % self.id, self.title

class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(128))
    created_date = db.Column(db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    modified_date = db.Column(db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Article %r %s>' % self.id, self.word

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    file_name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    size = db.Column(db.Integer)

    def __repr__(self):
        return '<Article %r %s>' % self.id, self.url
