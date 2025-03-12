import json
import boto3 
import os

rekognition_client = boto3.client("rekognition")
sqs_client = boto3.client('sqs')

def lambda_handler(event, context):
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    
    response = rekognition_client.detect_labels(
        Image={'S3Object':{'Bucket': bucket_name, 'Name': file_name}},
        MaxLabels=10,
        MinConfidence=80
    )

    labels = [label['Name'] for label in response["Labels"]]

    # disparo pro sqs
    sqs_client.send_message(
        QueueUrl=os.environ['SQS_URL'],
        MessageBody=json.dumps({
            'bucket': bucket_name,
            'key': file_name,
            'labels': labels
        })
    )

    print(labels)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Processamento de labels realizado com sucesso",
        }),
    }