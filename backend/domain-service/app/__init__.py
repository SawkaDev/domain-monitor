from flask import Flask
from flask_cors import CORS
from app.extensions import db, migrate
from app.config import config
from sqlalchemy_utils import database_exists, create_database
import os

def create_app():
    app = Flask(__name__)

    # CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    CORS(app)

    config_name = os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app.models import Domain
        engine = db.engine
        if not database_exists(engine.url):
            create_database(engine.url)
        db.create_all()

    from app.api.v1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    return app
