from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from main.config import config_by_name


db = SQLAlchemy()

def create_app(config_name):
    from main.controller.xml_controller import xml_app
    from main.controller.queue_controller import queue_app
    from main.controller.excel_validations_controller import excel_validations_app
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.config['MAX_CONTENT-PATH']=16 * 1024 * 1024
    app.register_blueprint(xml_app)
    app.register_blueprint(queue_app)
    app.register_blueprint(excel_validations_app)
    db.init_app(app)

    return app
