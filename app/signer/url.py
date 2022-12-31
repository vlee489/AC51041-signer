import boto3
from botocore.exceptions import ClientError
from typing import Optional
import logging


class UrlSigner:
    """Handles URL pre-signing for S3"""
    def __init__(self, region: str, endpoint: str, key_id: str, access_key: str):
        self.__s3_client = boto3.client('s3', region_name=region, endpoint_url=endpoint, aws_access_key_id=key_id,
                                        aws_secret_access_key=access_key)

    def create_signed_link(self, file_path: str, bucket: str, expire_in: int = 1200) -> Optional[str]:
        try:
            response = self.__s3_client.generate_presigned_url('get_object',
                                                               Params={'Bucket': bucket, 'Key': file_path},
                                                               ExpiresIn=expire_in)
            return response
        except ClientError as e:
            logging.error(e)
            return None
