from flask import Flask
from flask_cors import CORS
from app.extensions import db, migrate
from app.config import config
from app.tasks.update_whois_records import init_scheduler
from app.tasks.rabbitmq_consumer import init_rabbitmq_consumer  # Add this import
import os
import logging

def create_app():
    app = Flask(__name__)
    CORS(app)
    logging.basicConfig(level=logging.INFO)
    
    config_name = os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    init_scheduler(app)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app.models import whois
        db.create_all()

    from app.api.v1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    init_rabbitmq_consumer(app)

    return app
