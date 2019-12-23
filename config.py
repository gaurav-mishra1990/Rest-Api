import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = ""


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config_dict = {
    "development": "config.DevelopmentConfig",
    "testing": "config.TestingConfig",
    "staging": "config.StagingConfig",
    "production": "config.ProductionConfig",
    "default": "config.DevelopmentConfig"
}

config = config_dict["default"]

DB_HOST_NAME = os.environ.get("DB_HOST_NAME")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

Config.SQLALCHEMY_DATABASE_URI = "postgres://{}:{}@{}:{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST_NAME, DB_PORT, DB_NAME)

try:
    flask_configuration = os.environ.get("FLASK_ENV")
    config = config_dict[flask_configuration]
except Exception:
    pass


     