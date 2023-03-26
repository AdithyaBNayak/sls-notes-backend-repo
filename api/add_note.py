import boto3
import os
import json
import uuid
import time
import datetime
from aws_lambda_powertools import Logger
from api import util

logger = Logger()

# Get the DDB service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['NOTES_TABLE'])


@logger.inject_lambda_context
def add_note(event, context):
    logger.info(event)
    item = json.loads(event.get('body'))
    item['user_id'] = util.get_user_id(event['headers'])
    item['user_name'] = util.get_user_name(event['headers'])
    item['notes_id'] = item['user_id'] + ':' + uuid.uuid4()
    item['timestamp'] = str(time.time())
    item['expires'] = time.time() + datetime.timedelta(days=90)

    logger.info(item)

    table.put_item(Item=item)
    return {
        'statusCode': 200,
        'headers': util.getResponseHeaders(),
        'body': json.dumps(item)
    }

