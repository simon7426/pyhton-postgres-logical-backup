import os

import boto3


def get_s3_client(access_key, aws_secret_key, endpoint):
    session = boto3.session.Session()
    client = session.client(
        service_name="s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=aws_secret_key,
        endpoint_url=endpoint,
        use_ssl=False,
    )
    return client


def upload_to_s3(s3_client, bucket_name, bucket_path, file_full_path, dest_file):
    try:
        s3_client.upload_file(file_full_path, bucket_name, f"{bucket_path}/{dest_file}")
        os.remove(file_full_path)
    except boto3.exceptions.S3UploadFailedError as exc:
        print(exc)
        exit(1)
