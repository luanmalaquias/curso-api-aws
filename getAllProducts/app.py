import json
import boto3
import os

s3_client = boto3.client('s3')
dynamodb_resource = boto3.resource("dynamodb")

table_name = os.environ['TABLE_NAME']
table = dynamodb_resource.Table(table_name)

def read_all():
    response = table.scan()
    return response.get('Items', [])

def lambda_handler(event, context):
    items = read_all()
    print(items)
    
    return {
        "statusCode": 200,
        'headers':{
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin' : '*'
        },
        "body": json.dumps({
            'items': items,
        }),
    }