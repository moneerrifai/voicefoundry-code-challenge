import json
import boto3
import logging
from botocore.config import Config
import os
import csv
import random

# set retries 
config = Config(retries = {'max_attempts': 10})

# set region and other environmental variables
# region = os.environ['region']
region = 'us-east-1'
data_bucket = os.environ['data_bucket']
#data_bucket = 'voicefoundry-code-challenge-data'
# data_key = 
data_key = 'earnedpoints.csv'
# table name
table_name = 'husband-points-table'

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')

# Suppress boto3 logging
logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)

def generate_uniquekey():

    # a function that generates a unique key that will be used as the partition key

    return round(random.random()* 100000)


def write_data(table, row, key):

    # a function that inserts data into a dynamoDB table

    date = row['date']
    description = row['description']
    points = row['points']

    table.put_item(
        Item={
            'entry_id': key,
            'date': date,
            'description': description,
            'points': points
        }
    )


def lambda_handler(event, context):

    # a Lambda function that extracts data from S3, and inserts it into DynamoDB

    # log event
    logger.info(json.dumps(event))

    # create boto3 resources
    s3_resource = boto3.resource('s3', config=config)
    dynamodb_resource = boto3.resource('dynamodb', config=config)

    # using s3 resource, create a bucket sub-resource
    s3_bucket = s3_resource.Bucket(data_bucket)

    # using dynamodb resource, create a table sub-resource
    table = dynamodb_resource.Table(table_name)

    # download the contents of the .csv file to /tmp
    s3_bucket.download_file(data_key, '/tmp/earnedpoints.csv')

    # process file using the csv library, loop through each row, and write it to DynamoDB
    with open('/tmp/earnedpoints.csv', 'r') as file:
        csvreader = csv.DictReader(file, delimiter=',')
        next(csvreader, None) #skip the headers of the csv file
        for row in csvreader:
            # upload contents of each row to dynamodb table
            unique_key = generate_uniquekey()
            write_data(table, row, unique_key)

    return 'success'