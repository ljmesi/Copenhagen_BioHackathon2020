#!/usr/bin/env python3
import json
import yaml
import os
from abc import ABCMeta, abstractmethod

import boto3

DB_SECRET_FIELDS = [
        "username",
        "password",
        "host",
        "port",
        "dbname",
    ]

class Secret(metaclass=ABCMeta):
    def __init__(self, location):
        self.location = location

    @abstractmethod
    def parse_secret(self, location):
        raise NotImplementedError()

    def parse_yaml(self, file_path):
        with open(file_path) as yml:
            return yaml.load(yml, Loader=yaml.FullLoader)



class AwsSecret(Secret, metaclass=ABCMeta):
    FIELD_SECRET_STRING = "SecretString"
    SECRET_MANAGER_SERVICE = "secretsmanager"

    def __init__(self):
        client = boto3.client(self.SECRET_MANAGER_SERVICE)
        secret = client.get_secret_value(SecretId=self.get_secret_id())
        self.parse_secret(secret[self.FIELD_SECRET_STRING])

    @abstractmethod
    def get_secret_id(self):
        raise NotImplementedError()


class DbCredentials(AwsSecret):
    SECRET_ID = "DbCredentials"

    def get_secret_id(self):
        return self.SECRET_ID

    def parse_secret(self, secret):
        decoded_secret = json.loads(secret)
        for field in DB_SECRET_FIELDS:
            setattr(self, field, decoded_secret[field])

class LocalDbCredentials(Secret):
    def __init__(self, location):
        super().__init__(location)
        self.parse_secret()
    def parse_secret(self, location=None):
        if not location:
            location = self.location
        if os.path.exists(location) and os.path.isfile(location):
            if self.location.endswith(".yaml"):
                decoded_secret = self.parse_yaml(location)
                for field in DB_SECRET_FIELDS:
                    setattr(self, field, decoded_secret['database'][field])
