import json
from abc import ABCMeta, abstractmethod

import boto3


class AwsSecret(metaclass=ABCMeta):
    FIELD_SECRET_STRING = "SecretString"
    SECRET_MANAGER_SERVICE = "secretsmanager"

    def __init__(self):
        client = boto3.client(self.SECRET_MANAGER_SERVICE)
        secret = client.get_secret_value(SecretId=self.get_secret_id())
        self.parse_secret(secret[self.FIELD_SECRET_STRING])

    @abstractmethod
    def get_secret_id(self):
        raise NotImplementedError()

    @abstractmethod
    def parse_secret(self, secret):
        raise NotImplementedError()


class DbCredentials(AwsSecret):
    SECRET_ID = "DbCredentials"
    SECRET_FIELDS = [
        "username",
        "password",
        "host",
        "port",
        "dbname",
    ]

    def get_secret_id(self):
        return self.SECRET_ID

    def parse_secret(self, secret):
        decoded_secret = json.loads(secret)
        for field in self.SECRET_FIELDS:
            setattr(self, field, decoded_secret[field])
