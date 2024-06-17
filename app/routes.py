import io
import random
import os
import uuid
from minio.commonconfig import Tags
from flask import request, jsonify, Blueprint
from app import db
from app.minio import upload_object
from app.models import Drone, Task, Image
from PIL import Image as PILImage

core = Blueprint('core', __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
BUCKET_NAME = os.environ.get("MINIO_BUCKET")


@core.route('/drones', methods=['GET'])
def get_drones():
    drones = Drone.query.all()
    return jsonify([{'id': drone.id, 'name': drone.name} for drone in drones])


@core.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(name=data['name'], description=data['description'], drone_id=data['drone_id'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id}), 201


@core.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify({'id': task.id, 'name': task.name, 'description': task.description, 'drone_id': task.drone_id})


@core.route('/tasks/<int:id>/execute', methods=['POST'])
def execute_task(id):
    task = Task.query.get_or_404(id)
    images = generate_image(task_id=task.id, drone_id=task.drone_id)
    for image in images:
        new_image = Image(id=image.get('image_id'), etag=image.get('etag'), path=image.get('path'), task_id=task.id)
        db.session.add(new_image)
    db.session.commit()
    return jsonify({'status': 'Task executed and images captured'}), 200


@core.route('/tasks/<int:id>/images', methods=['GET'])
def get_task_images(id):
    images = Image.query.filter_by(task_id=id).all()
    return jsonify([{'id': image.id, 'path': image.path} for image in images])


def generate_image(task_id, drone_id):
    images = []
    for i in range(5):
        image = PILImage.effect_noise((500, 500), random.randint(10, 100))
        with io.BytesIO() as buf:
            image.save(buf, format='PNG')
            bytes_len = buf.getbuffer().nbytes
            buf.seek(0)

            image_id = uuid.uuid4().int >> (128 - 32)
            tags = Tags.new_object_tags()
            tags['Task'] = str(task_id)
            tags['Drone'] = str(drone_id)

            uploaded = upload_object(filename=f'{image_id}.png', data=buf, length=bytes_len, tags=tags)

            images.append({
                'id': image_id,
                'path': f'{uploaded.bucket_name}/{uploaded.object_name}',
                'etag': uploaded.etag
            })
    return images
