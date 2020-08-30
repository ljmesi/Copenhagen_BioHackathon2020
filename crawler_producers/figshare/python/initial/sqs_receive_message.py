import boto3

#TODO: check if in AWS, then try without credentials:
sqs_client = boto3.client('sqs', region_name='eu-central-1')

#settings = {}
#settings['AWS_SERVER_PUBLIC_KEY'] = 'YOUR_KEY'
#settings['AWS_SERVER_SECRET_KEY'] = 'YOUR_SECRET_KEY'
#settings['REGION_NAME'] = 'eu-central-1'
##sqs_client = boto3.client('sqs',aws_access_key_id=settings['AWS_SERVER_PUBLIC_KEY'],
#                      aws_secret_access_key=settings['AWS_SERVER_SECRET_KEY'],
#                      region_name=settings['REGION_NAME'])

queue_url = 'https://sqs.eu-central-1.amazonaws.com/397254617684/crawler_queue'

def receive_message():
    return sqs_client.receive_message(
    QueueUrl='https://sqs.eu-central-1.amazonaws.com/397254617684/crawler_queue',
    AttributeNames=['All'],
    MaxNumberOfMessages=10)

if __name__ == '__main__':
    resp = receive_message()
    print(resp)

#sample data:
#{'Messages': [{'MessageId': '98f4b739-8ae6-44f3-8fb9-e3806c0cf502', 'ReceiptHandle': 'AQEBMeD5qc5w2UIlTv6u8IYuo+QkgC0KuWdgnXxcdaSoXpmSWk0mCMnMcfSZilZ2gO1p+JAOimWldL13AwdagA1E8ifhNMnoTBLML39B10uEo9ksY7i3znWcGYfJWmdIOV6FY55ycwkHcWOUUUDSJSdTkAGSRVyXm55DdZ+SFkvUT2WsoKw6Lu/fozXLyydbQuk9/ghl7TSYV9BG5M8G2nTU6tFfPqJH7lfOYziNp87ihe+m8r7tE+U5Vu6xWsVOClAcCta+wdi6r8orfQnwXjVr40l4JHjADevTh+TuTnHfG7c/xJ/+RiKQPqh+55FvEbR6uRtYtit51IuYa+1+rA8/ey6TpupCe5/sFH0bmUaT74QVtpwNAYzrC/YcY7KLZ67quNhkIN/R8WxMDtxfxV3law==', 'MD5OfBody': 'be2f2b71f8fd0117b068202c69898782', 'Body': '{"title": "test title", "source_url": "https://figshare.com/search?q=.dcd", "keywords": ["keyword1", "keyword2"], "files": [{"file_name": "test_file", "url": "https://fileurl.com", "size": "24kb"}], "digital_object_id": "DOI.test.string", "parent_request_url": null, "description": "Test description", "parse_date": "04-04-2020:12:01:01"}', 'Attributes': {'SenderId': 'AROAVY7RYNJKF6LGEYJVX:i-0296cbce3a3bca116', 'ApproximateFirstReceiveTimestamp': '1593985332037', 'ApproximateReceiveCount': '1', 'SentTimestamp': '1593985322757'}}], 'ResponseMetadata': {'RequestId': '17fc58a7-df27-5c39-8faf-0fdb9453b2d6', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '17fc58a7-df27-5c39-8faf-0fdb9453b2d6', 'date': 'Sun, 05 Jul 2020 21:42:12 GMT', 'content-type': 'text/xml', 'content-length': '1747'}, 'RetryAttempts': 0}}
