import os
from app import client

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
BUCKET_NAME = os.environ.get("MINIO_BUCKET")


def upload_object(filename, data, length):
    found = client.bucket_exists(BUCKET_NAME)
    if not found:
        client.make_bucket(BUCKET_NAME)
    client.put_object(BUCKET_NAME, filename, data, length)