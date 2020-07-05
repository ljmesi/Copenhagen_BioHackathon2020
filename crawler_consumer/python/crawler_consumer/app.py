#!/usr/bin/env python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import yaml
import datetime

SECRETS = 'secrets.yaml'
DB_CONNECTION = 'mysql+mysqlconnector://{user}:{password}@{server}/{db_name}'

def get_secrets():
  with open(SECRETS) as d:
     return yaml.load(d, Loader=yaml.FullLoader)

def get_db_connection():
  secrets = get_secrets()
  if (secrets):
    db_creds = secrets.get('database')
    return DB_CONNECTION.format(user=db_creds.get('user'),
                                password=db_creds.get('password'),
                                server=db_creds.get('server'),
                                db_name=db_creds.get('db_name'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_connection()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# engine = db.create_engine(DB_CONNECTION)
# connection = engine.connect()
# metadata = db.MetaData()

keywords = db.Table('keywords',
                    db.Column('keyword_id', db.Integer, db.ForeignKey('keyword.id'), primary_key=True),
                    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True)
                    )

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    source_url = db.Column(db.String(255))
    keywords = db.relationship('Keyword', secondary=keywords, lazy='subquery', passive_deletes=True,
                               backref=db.backref('articles', lazy=True))
    files = db.relationship('File', backref='article', lazy=True, passive_deletes=True)
    digital_object_id = db.Column(db.String(128), unique=True)
    parent_request_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    parse_date = db.Column(db.TIMESTAMP(timezone=True))
    created_date = db.Column(db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    modified_date = db.Column(db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(128), unique=True)
    created_date = db.Column(db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    modified_date = db.Column(db.TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Article %r, %s>' % (self.id, self.word)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'), nullable=False)
    file_name = db.Column(db.String(255))
    url = db.Column(db.String(255), unique=True)
    size = db.Column(db.Integer)

    def __repr__(self):
        return '<Article %r %s>' % self.id

if __name__ == '__main__':
    app.run()
