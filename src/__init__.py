from flask import Flask, g, jsonify, request
from flask_cors import CORS
from src.db import init_db, close_connection
from src.app import router


def create_app(database_path):
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        DATABASE=database_path
    )
    CORS(app)
    init_db(app)

    @app.teardown_appcontext
    def on_teardown(exception):
        close_connection()

    @app.errorhandler(404)
    def not_found(error):
        return dict(error='404 Not Found'), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return dict(success=False, error='405 Method Not Allowed'), 405

    app.register_blueprint(router)

    return app
