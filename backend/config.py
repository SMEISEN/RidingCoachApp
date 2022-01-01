import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class BaseConfig(object):

    FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = os.getenv('FLASK_SECRET')

    SWAGGER_SUPPORTED_SUBMIT_METHODS = os.getenv('SWAGGER_SUPPORTED_SUBMIT_METHODS')
    FLASK_RESTPLUS_API_KEY = os.getenv('FLASK_RESTPLUS_API_KEY')

    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, 'frontend/dist')

    FLASK_HOST = os.getenv('HOST')
    FLASK_PORT = os.getenv('PORT')
    FLASK_BASE_URL = f"{FLASK_HOST}:{FLASK_PORT}"


class Config(BaseConfig):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestConfig(BaseConfig):

    TESTING = True
    DEBUG = False  # https://github.com/ga4gh/ga4gh-server/issues/791#issuecomment-158547948
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_TEST')
