DEBUG = True
SECRET_KEY = 'zaraSeando1'

DATABASE = {
    'name': 'database/pastillas.db',
    'engine': 'peewee.SqliteDatabase',
}

CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = "localhost"
CELERY_REDIS_PORT = 6379
CELERY_REDIS_DB = 0

DEBUG_TB_INTERCEPT_REDIRECTS=False

BROKER_URL = 'redis://localhost:6379/0'
UPLOAD_FOLDER = '/tmp'
