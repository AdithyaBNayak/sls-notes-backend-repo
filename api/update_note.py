import boto3
import os
import json
import time
import datetime

from aws_lambda_powertools import Logger
from api import util

logger = Logger()

# Get the DDB service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['NOTES_TABLE'])


@logger.inject_lambda_context
def update_note(event, context):
    logger.info(event)
    item = json.loads(event.get('body'))
    item['user_id'] = util.get_user_id(event['headers'])
    item['user_name'] = util.get_user_name(event['headers'])
    item['expires'] = time.time() + datetime.timedelta(days=90)
    response = table.put_item(
        Item=item,
        ConditionExpression = '#t = :t',
        ExpressionAttributeNames={
            '#t' : 'timestamp'
        },
        ExpressionAttributeValues={
            ':t' : item.get('timestamp')
        }
    )
    logger.info(response)
    return {
        'statusCode': 200,
        'headers': util.getResponseHeaders(),
        'body': json.dumps('')
    }
