import io
import uuid
from minio.commonconfig import Tags
from PIL import Image as PILImage
import random
from app.minio import upload_object


def generate_image():
    image = PILImage.effect_noise((500, 500), random.randint(10, 100))
    image_id = uuid.uuid4().int >> (128 - 32)
    return image, image_id


def upload_image(image, image_id, task):
    tags = Tags.new_object_tags()
    tags['Task'] = str(task.id)
    tags['Drone'] = str(task.drone_id)
    with io.BytesIO() as buf:
        image.save(buf, format='PNG')
        buf.seek(0)
        uploaded = upload_object(filename=f'{image_id}.png', data=buf, length=buf.getbuffer().nbytes, tags=tags)
    return uploaded
