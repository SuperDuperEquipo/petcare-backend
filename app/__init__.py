import os
from flask import Flask
from app.config.config import config_by_name
from app.core.extensions import db, migrate, jwt, cors


def create_app():
    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_by_name[env])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    from app.auth.routes.auth_routes import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    from app.pets.routes.pet_routes import pets_bp

    app.register_blueprint(pets_bp, url_prefix="/api/v1/pets")

    from app.vaccines.routes.vaccine_routes import vaccine_bp

    app.register_blueprint(vaccine_bp, url_prefix="/api/v1")

    return app
