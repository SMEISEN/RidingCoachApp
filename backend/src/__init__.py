from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from backend.config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['DATABASE_URL'] = Config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

from backend.src import routes