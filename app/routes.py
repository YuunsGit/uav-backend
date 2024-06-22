from os import environ
from flask import request, jsonify, Blueprint, abort, send_file
from app import db
from app.helpers import generate_image, upload_image
from app.models import Drone, Task, Image
from app.minio import get_object

core = Blueprint('core', __name__)

BUCKET_NAME = environ.get("MINIO_BUCKET")


@core.route('/drones', methods=['GET'])
def get_drones():
    """ Get all drones. """
    drones = Drone.query.all()
    return jsonify(
        [{'id': drone.id, 'name': drone.name, 'taskCount': len(drone.tasks),
          'imagesCaptured': sum(len(task.images) for task in drone.tasks)} for drone in drones])


@core.route('/drones/<int:id>', methods=['GET'])
def get_drone(id):
    """ Get drone details by ID. """
    drone = Drone.query.get(id)
    if drone is None:
        abort(404, description="Drone was not found")
    return jsonify({
        'id': drone.id,
        'name': drone.name,
        'taskCount': len(drone.tasks),
        'imagesCaptured': sum(len(task.images) for task in drone.tasks),
        'tasks': [{
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'images': [{'id': image.id, 'etag': image.etag, 'path': image.path} for image in task.images]
        } for task in drone.tasks]
    })


@core.route('/tasks', methods=['GET'])
def get_tasks():
    """ Get all tasks. """
    tasks = Task.query.all()
    return jsonify(
        [{'id': task.id, 'name': task.name, 'description': task.description, 'imageCount': len(task.images),
          'assignedTo': task.drone.name} for task in
         tasks])


@core.route('/tasks', methods=['POST'])
def create_task():
    """ Create a new task. """
    data = request.get_json()
    new_task = Task(name=data['name'], description=data['description'], drone_id=data['drone_id'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id}), 201


@core.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    """ Get task details by ID. """
    task = Task.query.get(id)
    if task is None:
        abort(404, description="Task was not found")
    return jsonify({
        'id': task.id,
        'name': task.name,
        'description': task.description,
        'imageCount': len(task.images),
        'assignedTo': task.drone.name,
        'images': [{'id': image.id, 'etag': image.etag, 'path': image.path} for image in task.images]
    })


@core.route('/tasks/<int:id>/execute', methods=['POST'])
def execute_task(id):
    """ Execute a task. """
    task = Task.query.get(id)
    if task is None:
        abort(404, description="Task was not found")
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
    """ Get all images for a task. """
    task = Task.query.get(id)
    if task is None:
        abort(404, description="Task was not found")
    return jsonify([{'id': image.id, 'path': image.path, 'etag': image.etag} for image in task.images])


@core.route('/images/<int:id>', methods=['GET'])
def get_image(id):
    """ Get image details by ID. """
    image = Image.query.get(id)
    if image is None:
        abort(404, description="Image was not found")
    try:
        return send_file(get_object(id), mimetype='image/png', as_attachment=True, download_name=f'{id}.png')
    except Exception as e:
        abort(500, description="Error occurred while retrieving the image: " + str(e))
