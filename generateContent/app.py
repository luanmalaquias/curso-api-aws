import json
import boto3 
import os
import uuid
from datetime import datetime

bedrock_client = boto3.client('bedrock-runtime')
dynamodb_resource = boto3.resource("dynamodb")

model_id = os.environ['MODEL_ID']
prompt_title = os.environ['PROMPT_TITLE']
prompt_description = os.environ['PROMPT_DESCRIPTON']
table_name = os.environ['TABLE_NAME']



table = dynamodb_resource.Table(table_name)

def save_to_dynamo(item_id, title, content, labels, qrcode):
    item = {
        'id': item_id,
        'createdAt': datetime.now().isoformat(),
        'title': title,
        'content': content,
        'labels': labels,
        'modelId': model_id,
        'qrcode': qrcode
    }
    table.put_item(Item=item)
    return item_id

def invoke_bedrock(prompt):
    request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 100,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]
    }

    json_request = json.dumps(request)
    response = bedrock_client.invoke_model(modelId=model_id, body=json_request)

    model_response = json.loads(response['body'].read())

    text_response = model_response['content'][0]['text']
    print(text_response)

    return text_response

def lambda_handler(event, context):
    lambda_client = boto3.client('lambda')

    print("Starting generateContent Lambda")
    
    if 'Records' in event:
        for record in event['Records']:
            message_body = json.loads(record['body'])
            
            labels = message_body.get('labels',{})
            prompt_title_final = f"{prompt_title}  {', '.join(labels)}"
            response_title = invoke_bedrock(prompt_title_final)
            prompt_description_final = f"{prompt_description} Etiquetas:{', '.join(labels)} Titulo do Produto:{response_title}"
            response_description = invoke_bedrock(prompt_description_final)
            
            print("Calling GenerateQrCode Lambda")

            item_id = str(uuid.uuid4())
            # save_to_dynamo(item_id, response_title, response_description, labels, null)

            payload = {
                "key1": item_id
            }

            response = lambda_client.invoke(
                FunctionName="GenerateQrCodeFunction",
                InvocationType="RequestResponse",
                Payload=json.dumps(payload)
            )

            response_payload = json.load(response['Payload'])

            if response_payload['statusCode'] == 200:
                item_id = save_to_dynamo(item_id, response_title, response_description, labels, response_payload['qrcodepath'])
                return {
                    "statusCode": 200,
                    "body": response_payload
                }
            else:
                print("Erro ao invocar a segunda lambda")
            