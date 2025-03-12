
import qrcode
import boto3
import os

s3_client = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']
AWS_REGION = os.environ.get("AWS_REGION", "us-east-2")

def lambda_handler(event, context):
    print("Starting generateQrCode Lambda")
    try:
        item_id = event["key1"]
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(item_id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        local_path = f"/tmp/{item_id}.png"
        img.save(local_path)

        s3_path = f"qrcodes/{item_id}.png"
        s3_client.upload_file(local_path, BUCKET_NAME, s3_path, ExtraArgs={"ContentType": "image/png"})
        s3_url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_path}"

        return {
            'statusCode': 200,
            'qrcodepath': s3_url
        }
    
    except Exception as e:
        print(f"Erro ao gerar QR code: {str(e)}")
        return {
            'statusCode': 500,
            'message': 'Erro ao gerar QR code'
        }