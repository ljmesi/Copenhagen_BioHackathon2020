import boto3

settings = {}
settings['AWS_SERVER_PUBLIC_KEY'] = 'YOUR_KEY'
settings['AWS_SERVER_SECRET_KEY'] = 'YOUR_SECRET_KEY'
settings['REGION_NAME'] = 'eu-central-1'

# Create SQS client
client = boto3.client('sqs',aws_access_key_id=settings['AWS_SERVER_PUBLIC_KEY'],
                      aws_secret_access_key=settings['AWS_SERVER_SECRET_KEY'],
                      region_name=settings['REGION_NAME'])


queue_url = 'https://sqs.eu-central-1.amazonaws.com/397254617684/crawler_queue'

# Send message to SQS queue
#TODO: check if message attributes or messaage body is more suitable
response = client.send_message(
    QueueUrl=queue_url,
    DelaySeconds=1,
    MessageAttributes={
        'SourceUrl': {
            'DataType': 'String',
            'StringValue': 'https://figshare.com/search?q=.dcd'
        },
        'StudyTitle': {
            'DataType': 'String',
            'StringValue': 'test title'
        },
        'KeywordList': {
            'DataType': 'String',
            'StringValue': "['dcd', 'ace-2', 'receptor']"
        },
        'Description': {
            'DataType': 'String',
            'StringValue': "test description"
        },
        'AuthorList': {
            'DataType': 'String',
            'StringValue': "['bob', 'alice', 'jane']"
        },
        'CategoryList': {
            'DataType': 'String',
            'StringValue': "['dcd', 'study']"
        },
        'PublishDate': {
            'DataType': 'String',
            'StringValue': "04-04-2020:12:01:01"
        },
        'DocumentList': {
            'DataType': 'String',
            'StringValue': "['study_document_1.dcd', 'study_document_2.dcd']"
        }
    },
    MessageBody=(
        'https://figshare.com/search?q=.dcd'
    )
)

print(response['MessageId'])