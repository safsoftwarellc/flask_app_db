from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from main.config import config_by_name


db = SQLAlchemy()

def create_app(config_name):
    from main.controller.xml_controller import xml_app
    from main.controller.queue_controller import queue_app
    from main.controller.excel_validations_controller import excel_validations_app
    from main.controller.sql_db_controller import sql_db_app
    from main.controller.user_db_controller import user_info_app
    from main.controller.test_scripts_contrller import test_scripts_app
    from main.controller.message_db_controller import message_app
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.config['MAX_CONTENT-PATH']=16 * 1024 * 1024
    app.register_blueprint(xml_app)
    app.register_blueprint(queue_app)
    app.register_blueprint(excel_validations_app)
    app.register_blueprint(sql_db_app)
    app.register_blueprint(user_info_app)
    app.register_blueprint(test_scripts_app)
    app.register_blueprint(message_app)
    db.init_app(app)

    return app
