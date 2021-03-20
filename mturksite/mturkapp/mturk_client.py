import boto3
from django.conf import settings

def mturk_client():
    mturk = boto3.client('mturk',
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
        region_name = settings.AWS_REGION_NAME,
        endpoint_url = settings.AWS_ENDPOINT_URL
    )
    return mturk