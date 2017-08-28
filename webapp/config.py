import os
from os.path import abspath, dirname, join

basedir = abspath(dirname(__file__))

class Config:
    "SECRET_KEY" = "1F9HClu5BiUu5MT6xvAf"
    "SQLALCHEMY_COMMIT_ON_TEARDOWN" = True
    "SQLALCHEMY_TRACK_MODIFICATIONS" = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    dbase_path = "sqlite:///" + join(basedir, "database-dev.sqlite")
    
class ProductionConfig(Config):
    DEBUG = True
    dbase_path = "sqlite:///" + join(basedir, "database.sqlite")


config = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "default": DevelopmentConfig
        }
