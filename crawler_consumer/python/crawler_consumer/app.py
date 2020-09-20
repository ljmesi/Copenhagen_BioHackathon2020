#!/usr/bin/env python3
import datetime

from flask import Flask

import yaml
import logging
from flask.json import JSONEncoder
from lib.secrets import DbCredentials, LocalDbCredentials
#from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

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

