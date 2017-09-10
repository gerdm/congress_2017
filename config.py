import os
from os.path import abspath, dirname, join

basedir = abspath(dirname(__file__))

class Config:
    SECRET_KEY = "1F9HClu5BiUu5MT6xvAf"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + join(basedir, "database.sqlite")
    
class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgres://ftsiumhnodtdvh:078cbbc380a50b2695a63bdb1fa46600b65a45197ce44f3a7289627a95233629@ec2-107-22-173-160.compute-1.amazonaws.com:5432/dftpi7njrgctsk"


config = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "default": DevelopmentConfig,
        "heroku": ProductionConfig
        }
