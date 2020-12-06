import os
import boto3
from botocore.config import Config
import logging
import json
import random

# set retries using the boto3 config
config = Config(retries = {'max_attempts': 10})

table_name = os.environ['dynamodb_table']

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


def lambda_handler(event, context):

    # this lambda function creates an entry in the Husbands Points database

    # log the event passed to lambda
    logger.info(json.dumps(event))

    # extract the data using json.loads which turns a string object into a python dict
    data = json.loads(json.loads(event['body'])['input'])
    
    # create dynamodb boto3 resource
    dynamodb_resource = boto3.resource('dynamodb', config=config)

    # using dynamodb resource, create a table sub-resource
    table = dynamodb_resource.Table(table_name)

    # set entry
    item = {
        'entry_id': generate_uniquekey(),
        'date': data['date'],
        'description': data['description'],
        'points': data['points'],
    }

    # add the entry to the dynamodb table
    try:
        table.put_item(Item=item)
        logger.info(f'Added the following item to the DynamoDB table: {item}')
    except Exception as e:
        logger.error(e)
        raise e
        return {
            "statusCode": 400,
            "body": json.dumps(str(e))
        }

    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response