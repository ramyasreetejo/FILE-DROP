import boto3
from botocore.client import Config
from io import BytesIO
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

bucket_name = str(os.getenv('AWS_S3_BUCKET_NAME'))

# MinIO Configuration
aws_access_key_id=str(os.getenv('AWS_ACCESS_KEY_ID'))
aws_secret_access_key=str(os.getenv('AWS_SECRET_ACCESS_KEY'))
endpoint_url = str(os.getenv('MINIO_ENDPOINT_URL'))

# Initialize S3 client
s3 = boto3.client(
    's3',
    endpoint_url=endpoint_url,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    config=Config(signature_version='s3v4')
)

# Function to create a bucket
def create_bucket(bucket_name):
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")
    except Exception as e:
        print(f"Error creating bucket: {str(e)}")

if __name__ == "__main__":
    create_bucket(bucket_name)
