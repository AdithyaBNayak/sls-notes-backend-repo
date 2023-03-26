import boto3
import os
import json

from aws_lambda_powertools import Logger
from api import util

logger = Logger()

# Get the DDB service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['NOTES_TABLE'])


@logger.inject_lambda_context
def delete_note(event, context):
    logger.info(event)
    timestamp = event['pathParameters'].get('timestamp')

    response = table.delete_item(
        Key={
            'user_id': util.get_user_id(event['headers']),
            'timestamp': timestamp
        }
    )
    logger.info(response)
    return {
        'statusCode': 200,
        'headers': util.getResponseHeaders()
    }
