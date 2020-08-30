import boto3
import json

# TODO: check if in AWS, then try without credentials:
sqs_client = boto3.client('sqs', region_name='eu-central-1')
# settings = {}
# settings['AWS_SERVER_PUBLIC_KEY'] = 'YOUR_KEY'
# settings['AWS_SERVER_SECRET_KEY'] = 'YOUR_SECRET_KEY'
# settings['REGION_NAME'] = 'eu-central-1'
##sqs_client = boto3.client('sqs',aws_access_key_id=settings['AWS_SERVER_PUBLIC_KEY'],
#                      aws_secret_access_key=settings['AWS_SERVER_SECRET_KEY'],
#                      region_name=settings['REGION_NAME'])

#sqs_client = boto3.client('sqs')

queue_url = 'https://sqs.eu-central-1.amazonaws.com/397254617684/crawler_queue'


# Send message to SQS queue
# example
def send_message():
    test_article = dict()
    test_article['title'] = 'test title'
    test_article['source_url'] = 'https://figshare.com/search?q=.dcd'
    test_article['keywords'] = ['keyword1', 'keyword2']
    test_article['files'] = ['study_document_1.dcd', 'study_document_2.dcd']
    test_article['digital_object_id'] = "DOI.test.string"
    test_article['parent_request_url'] = None  # used in secondary parsing
    test_article['description'] = "Test description"
    test_article['parse_date'] = "04-04-2020:12:01:01"
    test_article['files'] = [{"file_name": "test_file", "url": "https://fileurl.com", "size": "24kb"}]
    return sqs_client.send_message(
        QueueUrl=queue_url,
        DelaySeconds=1,
        MessageBody=(
            # validate json, validate DTO keys
            json.dumps(test_article)
        )
    )


if __name__ == '__main__':
    response = send_message()
    print(response['MessageId'])
