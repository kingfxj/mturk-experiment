import boto3

def mturk_client():
    mturk = boto3.client('mturk',
        aws_access_key_id = "PASTE_YOUR_IAM_USER_ACCESS_KEY",
        aws_secret_access_key = "PASTE_YOUR_IAM_USER_SECRET_KEY",
        region_name='us-east-1',
        endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
    )

    return mturk