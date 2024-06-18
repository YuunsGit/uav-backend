import os
from flask import request, jsonify, Blueprint
from app import db
from app.helpers import generate_image, upload_image
from app.models import Drone, Task, Image

core = Blueprint('core', __name__)

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
    for i in range(5):
        image, image_id = generate_image()
        uploaded = upload_image(image, image_id, task)
        new_image = Image(id=image_id, etag=uploaded.etag, path=f'{uploaded.bucket_name}/{uploaded.object_name}',
                          task_id=task.id)
        db.session.add(new_image)
    db.session.commit()
    return jsonify({'status': 'Task executed and images captured'}), 200


@core.route('/tasks/<int:id>/images', methods=['GET'])
def get_task_images(id):
    images = Image.query.filter_by(task_id=id).all()
    return jsonify([{'id': image.id, 'path': image.path, 'etag': image.etag} for image in images])
