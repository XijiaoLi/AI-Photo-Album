import json
import boto3
import urllib
import re
from botocore.vendored import requests
# from requests_aws4auth import AWS4Auth
from datetime import datetime



# access_key='AKIAXGHK2XQJZL2Q6CCW'
# secret_key='/d2qSRugBAsHhuzGVbAQ8LdKWZW4omC88j834QLz'


region = 'us-east-1' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
# awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://vpc-photos-um6blvqixup6knzqyrqiji4zoa.us-east-1.es.amazonaws.com'
index = 'photos'
type = '_doc'
url = host + '/' + index + '/' + type
headers = { "Content-Type": "application/json" }

rekognition = boto3.client('rekognition')

createdTimestamp = str(datetime.now())

def lambda_handler(event, context):
    # get bucket name and photo name
    bucket = event['Records'][0]['s3']['bucket']['name']
    photo = event['Records'][0]['s3']['object']['key']
    # print(bucket)
    # print(photo)
    # call get_lables
    try:
        labels = get_labels(bucket, photo)
        # print(lables)
        # return(labels)
        # labels = ['a','b']
    except Exception as e:
        print(e)
    message = {
        'objectKey': photo,
        'bucket': bucket,
        'createdTimestamp': createdTimestamp,
        'labels': labels
    }
    
    message = json.dumps(message, indent=2)
    r = requests.post(url, data=message, headers=headers)
    print(r)

    
def get_labels(bucket_name, photo_name):
    # print(bucket_name)
    # print(photo_name)
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': photo_name,
            }
        },
        MaxLabels=8,
        MinConfidence=70
        
    )
    labels = []
    for label_info in response['Labels']:
        labels.append(label_info['Name'].lower())
    return labels