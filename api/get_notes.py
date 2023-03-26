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
def get_notes(event, context):

    logger.info(event)
    query = event.get('queryStringParameters',{})
    limit = query.get('limit',5)

    user_id = util.get_user_id(event['headers'])
    start_timestamp = query.get('start', 0)

    data = query_table(limit, user_id, start_timestamp)
    logger.info(data)
    return {
        'statusCode': 200,
        'headers': util.getResponseHeaders(),
        'body': json.dumps(data)
    }


def query_table(limit, user_id, start_timestamp):
    if start_timestamp > 0:
        response = table.query(
            Limit=limit,
            ScanIndexForward=False,
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={
                ':uid': user_id
            }
        )
    else:     
        response = table.query(
                Limit=limit,
                ScanIndexForward=False,
                KeyConditionExpression='user_id = :uid',
                ExpressionAttributeValues={
                    ':uid': user_id
                },
                ExclusiveStartKey={
                    'user_id': 'user_id',
                    'timestamp': start_timestamp
                }
            )
    return response

def query_without_start_key(limit, user_id, start_timestamp):
    response = table.query(
            Limit=limit,
            ScanIndexForward=False,
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={
                ':uid': user_id
            }
        )
    return response