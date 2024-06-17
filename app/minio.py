import os
from app import minio_client

BUCKET_NAME = os.environ.get("MINIO_BUCKET")


def upload_object(filename, data, length, tags):
    found = minio_client.bucket_exists(BUCKET_NAME)
    if not found:
        minio_client.make_.bucket(BUCKET_NAME)
    image = minio_client.put_object(BUCKET_NAME, filename, data, length, tags=tags)
    return image
