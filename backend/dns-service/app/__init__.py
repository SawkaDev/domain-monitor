from flask import Flask
from app.extensions import db, migrate, ma
from app.config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from app.api.v1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    return app
