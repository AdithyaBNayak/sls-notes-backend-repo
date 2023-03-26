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
def get_note(event, context):
    logger.info(event)
    notes_id = event['pathParameters'].get('notes_id')
    items = table.query(
            Limit=1,
            IndexName= 'notes_id-index',
            KeyConditionExpression='notes_id = :id',
            ExpressionAttributeValues={
                ':id': notes_id
            }
        )['Items']
    logger.info(items)
    
    if items: 
        return {
            'statusCode': 200,
            'headers': util.getResponseHeaders(),
            'body': json.dumps(items[0])
        }
    
    return {
            'statusCode': 404,
            'headers': util.getResponseHeaders()
        }
