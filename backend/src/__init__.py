import os
from flask import Flask, current_app, send_file, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_restplus import Api
from backend.config import Config

app = Flask(__name__, static_folder='../../frontend/dist/static', template_folder="../../frontend/dist")
app.config.from_object(Config())
blueprint = Blueprint('api', __name__, url_prefix='/api')
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(blueprint)
app.register_blueprint(blueprint)
CORS(app)

from backend.src.resources import MaintenanceResource, HistoryResource, BikeResource

api.add_resource(MaintenanceResource, '/maintenance/list')
api.add_resource(HistoryResource, '/maintenance/history')
api.add_resource(BikeResource, '/bike')


@app.route('/')
@app.route('/home')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)


@app.cli.command(name='create_tables')
def create_tables():
    db.create_all()


app.cli.add_command(create_tables)
