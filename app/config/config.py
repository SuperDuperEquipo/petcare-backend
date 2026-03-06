import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))
    )
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    @staticmethod
    def get_db_uri():
        user     = os.getenv("DB_USER", "petcare_user")
        password = os.getenv("DB_PASSWORD", "petcare_pass")
        host     = os.getenv("DB_HOST", "localhost")
        port     = os.getenv("DB_PORT", "3306")
        name     = os.getenv("DB_NAME", "petcare_db")
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = Config.get_db_uri()


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = Config.get_db_uri()


config_by_name = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
}