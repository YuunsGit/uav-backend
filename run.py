from app import create_app

flask_app = create_app()


@flask_app.route('/status', methods=['GET'])
def status():
    return 'OK!'


if __name__ == '__main__':
    flask_app.run(debug=True)
