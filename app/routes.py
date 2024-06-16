def register_routes(app, db):
    @app.route('/')
    def hello_world():
        return '<h1>Hello World</h1>'

