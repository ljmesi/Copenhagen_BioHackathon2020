import boto3
import os
import logging
from typing import List
from crawler_lib.article import Article
from mypy_boto3_sqs.client import SQSClient

FETCH_LIMIT = 10
BUILD_ATTEMPT_LIMIT = 5

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

SQS_URL = 'https://sqs.eu-central-1.amazonaws.com/397254617684/crawler_queue'

# REGION_NAME = os.environ.get('REGION_NAME')
SERVER_SECRET_KEY = os.environ.get('AWS_SERVER_SECRET_KEY')
SERVER_PUBLIC_KEY = os.environ.get('AWS_SERVER_PUBLIC_KEY')


class ArticleProducer(object):
    def __init__(self):
        self.client = None

    def build_client(self):
        pass

    def send_article(self, article: Article):
        pass


class FigshareArticleProducer(ArticleProducer):
    def __init__(self):
        super().__init__()

    def build_client(self) -> None:
        self.client = boto3.client('sqs', region_name='eu-central-1',
                                   aws_access_key_id=SERVER_PUBLIC_KEY,
                                   aws_secret_access_key=SERVER_SECRET_KEY)

    def get_client(self) -> SQSClient:
        if not self.client:
            self.build_client()
        return self.client

    def send_article(self, article: Article) -> str:
        client = self.get_client()
        return client.send_message(QueueUrl=SQS_URL,
                                   DelaySeconds=0,
                                   MessageBody=article.to_json())

    def send_articles(self, articles: List[Article]) -> List[str]:
        response_list = []
        client = self.get_client()
        for article in articles:
            client.send_message(QueueUrl=SQS_URL,
                                DelaySeconds=0,
                                MessageBody=article.to_json())
        return response_list

    def close_client(self):
        self.client = None
