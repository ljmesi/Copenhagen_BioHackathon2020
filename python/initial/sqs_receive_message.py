import boto3

settings = {}
settings['AWS_SERVER_PUBLIC_KEY'] = 'YOUR_KEY'
settings['AWS_SERVER_SECRET_KEY'] = 'YOUR_SECRET_KEY'
settings['REGION_NAME'] = 'eu-central-1'

sqs_client = boto3.client('sqs',aws_access_key_id=settings['AWS_SERVER_PUBLIC_KEY'],
                      aws_secret_access_key=settings['AWS_SERVER_SECRET_KEY'],
                      region_name=settings['REGION_NAME'])
resp = sqs_client.receive_message(
    QueueUrl='https://sqs.eu-central-1.amazonaws.com/397254617684/crawler_queue',
    AttributeNames=['All'],
    MaxNumberOfMessages=10
)

print(resp)
