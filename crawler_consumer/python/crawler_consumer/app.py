#!/usr/bin/env python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import datetime

DB_CONNECTION = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
user=<USERNAME>, password=<PASSWORD>, server=<SERVER>, database=<DATABASE>
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
    source_url = db.Column(db.String(128))
    keywords = db.relationship('Keyword', secondary=keywords, lazy='subquery',
    backref=db.backref('articles', lazy=True))
    created_date = db.Column(db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    modified_date = db.Column(db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(128))
    created_date = db.Column(db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    modified_date = db.Column(db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
