from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

app.config['SECRET_KEY'] = 'Som3$ec5etK*y'  # Required for Flask-WTF
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lab5_user:password@localhost/lab5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)



from app import views
from app.models import Movie  # Import your model