from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from ..config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.logger.setLevel(app.config["LOGGING_LEVEL"])
    db.init_app(app)

    from .api import api as api_blueprint
    from .api import not_found_error

    app.register_blueprint(api_blueprint, url_prefix="/")
    app.register_error_handler(404, not_found_error)

    @app.before_first_request
    def before_first_request():
        db.create_all()

    return app
