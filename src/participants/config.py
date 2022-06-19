import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SERVER_NAME = os.environ.get("SERVER_NAME")
    DATA_DIR = os.environ.get("DATA_DIR", os.getcwd())
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    LOGGING_LEVEL = "DEBUG"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(Config.DATA_DIR, "participants-dev.sqlite")
    SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO", "off").lower() in [
        "true",
        "1",
        "on",
    ]


class TestingConfig(Config):
    TESTING = True
    LOGGING_LEVEL = "INFO"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(Config.DATA_DIR, "participants-test.sqlite")


class ProductionConfig(Config):
    LOGGING_LEVEL = "INFO"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(Config.DATA_DIR, "participants.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
