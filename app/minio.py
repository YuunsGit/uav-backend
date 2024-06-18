from os import environ

from app import minio_client

BUCKET_NAME = environ.get("MINIO_BUCKET")


def upload_object(filename, data, length, tags):
    """ Upload an object to MinIO. """
    found = minio_client.bucket_exists(BUCKET_NAME)
    if not found:
        minio_client.make_bucket(BUCKET_NAME)
    image = minio_client.put_object(BUCKET_NAME, filename, data, length, tags=tags)
    return image
