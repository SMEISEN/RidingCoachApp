import os
import json
import click
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
from flask import Flask, Blueprint, current_app, send_file
from flask_cors import CORS
from backend.api import api
from backend.api.endpoints.maintenance import ns as maintenance_namespace
from backend.api.endpoints.history import ns as history_namespace
from backend.api.endpoints.bike import ns as bike_namespace
from backend.api.endpoints.training import ns as training_namespace
from backend.api.endpoints.setup import ns as setup_namespace
from backend.api.endpoints.coach import ns as coach_namespace
from backend.api.endpoints.email import ns as email_namespace
from backend.api.endpoints.session import ns as session_namespace
from backend.api.endpoints.laptime import ns as laptime_namespace
from backend.api.endpoints.sparepart import ns as sparepart_namespace
from backend.api.endpoints.sparepartitem import ns as sparepartitem_namespace
from backend.api.endpoints.tire import ns as tire_namespace
from backend.api.endpoints.maintenance import MaintenanceModel
from backend.api.endpoints.coach import CoachModel
from backend.config import Config
from backend.database import db, ma, migrate

index_bp = Blueprint('index', __name__)
favicon_bp = Blueprint('favicon', __name__)
assets_bp = Blueprint('assets', __name__)
cli = click.Group()


def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../frontend/dist/static', template_folder='../frontend/dist')
    app.url_map.strict_slashes = False
    app.config.from_object(config_class)

    api_bp = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(api_bp)
    api.add_namespace(maintenance_namespace)
    api.add_namespace(history_namespace)
    api.add_namespace(bike_namespace)
    api.add_namespace(training_namespace)
    api.add_namespace(setup_namespace)
    api.add_namespace(coach_namespace)
    api.add_namespace(email_namespace)
    api.add_namespace(session_namespace)
    api.add_namespace(laptime_namespace)
    api.add_namespace(sparepart_namespace)
    api.add_namespace(sparepartitem_namespace)
    api.add_namespace(tire_namespace)

    app.register_blueprint(api_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(favicon_bp)
    app.register_blueprint(assets_bp)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    CORS(app)

    app.cli.add_command(create_tables)
    app.cli.add_command(drop_tables)
    app.cli.add_command(clear_tables)

    return app


@index_bp.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)


@favicon_bp.route('/favicon.svg')
def favicon_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'favicon.svg')
    return send_file(entry)


@assets_bp.route('/assets/<path:file>')
def assets_client(file):
    # remove slashes, dots, and backslashes
    file = secure_filename(file)

    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'assets', file)
    return send_file(entry)


@cli.command(name='create_tables')
def create_tables():
    db.create_all()

    print('Database created!')


@cli.command(name='copy_maintenance_template')
@click.argument('temp', nargs=1)
def copy_maintenance_template(temp):

    with open(temp) as json_file:
        maintenance_template = json.load(json_file)

    for entry in maintenance_template.items():
        new_maintenance = MaintenanceModel(
            category=entry[1]['category'],
            name=entry[1]['name'],
            interval_amount=entry[1]['interval_amount'],
            interval_unit=entry[1]['interval_unit'],
            interval_type=entry[1]['interval_type'],
            datetime_created=datetime.now(timezone.utc),
            datetime_last_modified=datetime.now(timezone.utc),
        )
        db.session.add(new_maintenance)

    db.session.commit()

    print('Template copied into database!')


@cli.command(name='copy_coach_template')
@click.argument('temp', nargs=1)
def copy_coach_template(temp):

    with open(temp) as json_file:
        coach_template = json.load(json_file)

    for entry in coach_template:
        new_coach = CoachModel(
            category=entry['category'],
            symptom=entry['symptom'],
            notes=entry['notes'],
            questions=entry['questions'],
            advice=entry['advice'],
            datetime_created=datetime.now(timezone.utc),
            datetime_last_modified=datetime.now(timezone.utc),
        )
        db.session.add(new_coach)

    db.session.commit()

    print('Template copied into database!')


@cli.command(name='drop_tables')
def drop_tables():
    db.drop_all()
    print('Database dropped!')


@cli.command(name='clear_tables')
def clear_tables():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(f"Cleared table {table}!")
        db.delete(table)
    db.session.commit()
