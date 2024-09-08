import boto3
from botocore.client import Config
import io

class s3API:
    def __init__(self, aws_access_key_id, aws_secret_access_key, endpoint_url):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=Config(signature_version = 's3v4')
        )
        # MinIO requires endpoint_url and signature_version s3v4, these can be avoided incase of AWS S3

    def upload_to_s3(self, bucket_name, file_id, file_obj, file_type):
        self.s3_client.upload_fileobj(file_obj, bucket_name, file_id, ExtraArgs={'ContentType': file_type})

    def download_from_s3(self, bucket_name, file_id):
        file_obj = io.BytesIO()
        self.s3_client.download_fileobj(bucket_name, file_id, file_obj)
        file_obj.seek(0)  # Move to the beginning of the file object
        return file_obj.read()

    def delete_from_s3(self, bucket_name, file_id):
        self.s3_client.delete_object(Bucket=bucket_name, Key=file_id)
