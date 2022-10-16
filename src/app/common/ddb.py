import boto3
import os
from boto3.resources.base import ServiceResource


def initialize_db() -> ServiceResource:
    ddb = boto3.resource(
        "dynamodb",
        endpoint_url=os.environ.get("DYNAMO_ENDPOINT"),
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    return ddb
