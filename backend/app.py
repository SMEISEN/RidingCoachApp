import os
from flask import Flask, Blueprint, current_app, send_file
from flask_cors import CORS
from backend.api import api
from backend.api.endpoints.maintenance import ns as maintenance_namespace
from backend.api.endpoints.history import ns as history_namespace
from backend.api.endpoints.bike import ns as bike_namespace
from backend.config import Config
from backend.database import db, ma

app = Flask(__name__, static_folder='../frontend/dist/static', template_folder="../frontend/dist")
app.url_map.strict_slashes = False


def initialize_app(flask_app):
    flask_app.config.from_object(Config())

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)

    api.add_namespace(maintenance_namespace)
    api.add_namespace(history_namespace)
    api.add_namespace(bike_namespace)

    flask_app.cli.add_command(create_tables)
    flask_app.cli.add_command(drop_tables)
    flask_app.cli.add_command(clear_tables)

    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)
    ma.init_app(flask_app)

    CORS(flask_app)


@app.route('/')
@app.route('/home')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)


@app.cli.command(name='create_tables')
def create_tables():
    db.create_all()
    print('Database created!')


@app.cli.command(name='drop_tables')
def drop_tables():
    db.drop_all()
    print('Database dropped!')


@app.cli.command(name='clear_tables')
def clear_tables(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(f"Cleared table {table}!")
        session.execute(table.delete())
    session.commit()
