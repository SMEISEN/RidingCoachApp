from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS


app = Flask(__name__, static_folder='../../frontend/dist/static', template_folder="../../frontend/dist")
app.config.from_object('backend.config.Config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

from backend.src import routes