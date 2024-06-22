from os import environ

from minio import Minio

MINIO_API_HOST = environ.get("MINIO_ENDPOINT")
ACCESS_KEY = environ.get("MINIO_ROOT_USER")
SECRET_KEY = environ.get("MINIO_ROOT_PASSWORD")
BUCKET_NAME = environ.get("MINIO_BUCKET")

minio_client = Minio(MINIO_API_HOST, ACCESS_KEY, SECRET_KEY, secure=False)


def upload_object(filename, data, length, tags):
    """ Upload an object to MinIO. """
    found = minio_client.bucket_exists(BUCKET_NAME)
    if not found:
        minio_client.make_bucket(BUCKET_NAME)
    image = minio_client.put_object(BUCKET_NAME, filename, data, length, tags=tags)
    return image


def get_object(id):
    """ Get an object from MinIO. """
    image = minio_client.get_object(BUCKET_NAME, f'{id}.png')
    print('ImageRes', image)
    return image
