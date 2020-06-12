import os
import json
from datetime import datetime
from flask import Flask, Blueprint, current_app, send_file
from flask_cors import CORS
from flask_migrate import MigrateCommand
from backend.api import api
from backend.api.endpoints.maintenance import ns as maintenance_namespace
from backend.api.endpoints.maintenance import MaintenanceModel
from backend.api.endpoints.history import ns as history_namespace
from backend.api.endpoints.bike import ns as bike_namespace
from backend.config import Config
from backend.database import db, ma, migrate

app = Flask(__name__, static_folder='../frontend/dist/static', template_folder="../frontend/dist")
app.url_map.strict_slashes = False
app.config.from_object(Config())

blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)
api.add_namespace(maintenance_namespace)
api.add_namespace(history_namespace)
api.add_namespace(bike_namespace)

app.register_blueprint(blueprint)

db.init_app(app)
ma.init_app(app)
migrate.init_app(app, db)

CORS(app)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index_client(path):
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)


@app.cli.command(name='create_tables')
def create_tables():
    db.create_all()

    with open('backend/database/templates/maintenance_model_template.json') as json_file:
        maintenance_template = json.load(json_file)

    for entry in maintenance_template.items():
        new_maintenance = MaintenanceModel(
            category=entry[1]['category'],
            name=entry[1]['name'],
            interval_amount=entry[1]['interval_amount'],
            interval_unit=entry[1]['interval_unit'],
            interval_type=entry[1]['interval_type'],
        )
        db.session.add(new_maintenance)
    db.session.commit()

    print('Database created!')


@app.cli.command(name='drop_tables')
def drop_tables():
    db.drop_all()
    print('Database dropped!')


@app.cli.command(name='clear_tables')
def clear_tables():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(f"Cleared table {table}!")
        db.delete(table)
    db.session.commit()


app.cli.add_command(create_tables)
app.cli.add_command(drop_tables)
app.cli.add_command(clear_tables)
