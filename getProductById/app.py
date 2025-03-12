import json
import boto3
import os

s3_client = boto3.client('s3')
dynamodb_resource = boto3.resource("dynamodb")

table_name = os.environ['TABLE_NAME']
table = dynamodb_resource.Table(table_name)

def readItem(item_id):
    response = table.get_item(
        Key={
            'id': item_id
        }
    )
    return response.get('Item', 'Id not found')

def lambda_handler(event, context):
    item_id = event['pathParameters']['id']
    print(item_id)
    item = readItem(item_id)
    
    return {
        "statusCode": 200,
        'headers':{
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin' : '*'
        },
        "body": json.dumps({
            'item': item,
        }),
    }