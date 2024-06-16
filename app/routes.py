from flask import request, jsonify, Blueprint
from app import db
from app.models import Drone, Task, Image
import random
from PIL import Image as PILImage

core = Blueprint('core', __name__)


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
    image_paths = generate_dummy_images(task.id)
    for path in image_paths:
        new_image = Image(path=path, task_id=task.id)
        db.session.add(new_image)
    db.session.commit()
    return jsonify({'status': 'Task executed and images captured'}), 200


@core.route('/tasks/<int:id>/images', methods=['GET'])
def get_task_images(id):
    images = Image.query.filter_by(task_id=id).all()
    return jsonify([{'id': image.id, 'path': image.path} for image in images])


def generate_dummy_images(id):
    image_paths = []
    for i in range(5):
        image = PILImage.effect_noise((100, 100), random.randint(10, 100))
        path = f'static/images/task_{id}_image_{i}.png'
        image.save(path)
        image_paths.append(path)
    return image_paths
