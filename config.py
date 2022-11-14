import os
from datetime import timedelta


class BaseConfig:
    SECRET_KEY = 'hww44944i'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    PER_PAGE_COUNT = 10
    UPLOAD_IMAGE_PATH = "images"


class DevelopmentConfig(BaseConfig):
    # 数据库的配置变量
    HOSTNAME = '127.0.0.1'
    PORT = '80'
    DATABASE = 'pythonbbs'
    USERNAME = 'root'
    PASSWORD = 'hww74520i'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

    SQLALCHEMY_DATABASE_URI = DB_URI

    # 邮箱配置
    # 这里使用qq邮箱
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = "szvsxvawsg@qq.com"
    MAIL_PASSWORD = "bkclqnypqmssddih"
    MAIL_DEFAULT_SENDER = "szvsxvawsg@qq.com"

    # redis配置
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = '6379'

    # celery配置
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

    AVATARS_SAVE_PATH = os.path.join(BaseConfig.UPLOAD_IMAGE_PATH, "avatars")


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = ''


class ProductionConfig(BaseConfig):
    pass
