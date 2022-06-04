from flask import Flask, jsonify
import os
from src.constants.http_status_code import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.auth import auth
from src.btc import btc
from src.database import db
from src.config.swagger import template, swagger_config
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),

            SWAGGER={
                "title": "Crpyto API",
                "universion": 3
            }
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(btc)

    Swagger(app, config=swagger_config, template=template)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error": "Not found"}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({"error": "Something went wrong, we are working on it"}), HTTP_500_INTERNAL_SERVER_ERROR

    

    return app


