from flask import jsonify
from werkzeug.exceptions import HTTPException
from app import create_app

app = create_app()


@app.route('/status', methods=['GET'])
def status():
    """ Check the health status of the application. """
    return 'OK!'


@app.errorhandler(HTTPException)
def handle_exception(e):
    """ Return JSON instead of HTML for HTTP errors. """
    return jsonify({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }), e.code


if __name__ == '__main__':
    app.run(host='0.0.0.0')