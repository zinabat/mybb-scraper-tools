import json
import requests
import asyncio
import boto3
from getAllActive import getAllActiveChars

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    bucketName = 'wolfrpg-characters'
    bucket = s3.Bucket(bucketName)

    try:
        s3.meta.client.head_bucket(Bucket=bucketName)
    except boto3.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = e.response['Error']['Code']
        if error_code == '404':
            return {
                "statusCode": error_code,
                "body": "Bucket '{}' does not exist".format(bucketName)
            }
    result = asyncio.run(getAllActiveChars())
    # store in s3
    bucket.put_object(Body=bytes(result.encode('UTF-8')), Key='active-chars.json')
    return {
        "statusCode": 200,
        "body": result
    }
