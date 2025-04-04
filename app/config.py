import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env if it exists.
import os

# Define the base directory as the root of your project
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    # UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False