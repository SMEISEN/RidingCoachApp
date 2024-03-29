import json
import pytest
from sqlalchemy.orm.exc import NoResultFound
from backend.app import create_app
from backend.config import TestConfig
from backend.app import db
from backend.utils.uuid import validate_uuid

from backend.tests.api.requests.coach import get
from backend.tests.api.requests.coach import post
from backend.tests.api.requests.coach import get_item
from backend.tests.api.requests.coach import put_item
from backend.tests.api.requests.coach import delete_item
from backend.tests.api.requests.coach import default_payload_post, default_payload_put


@pytest.fixture(scope='module')
def app():
    # setup
    _app = create_app(TestConfig)

    # create test tables
    with _app.app_context():
        db.drop_all()
        db.create_all()

    yield _app

    # teardown
    with _app.app_context():
        db.drop_all()


@pytest.fixture(scope='module')
def client(app):
    _client = app.test_client()
    return _client


@pytest.fixture(scope='function')  # each test needs to create its own item
def coach_id(app, client):
    # create a new coach item
    response = post(app, client)
    _coach_id = json.loads(response.get_data())

    return _coach_id


def test_get(app, client):
    # GET /coach/
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty
    assert response.status_code == 200

    # post two coach items
    post(app, client, default_payload_post)
    post(app, client, default_payload_put)

    response = get(app, client)
    coach_items = json.loads(response.get_data())
    assert isinstance(coach_items, list)
    assert len(coach_items) == 2
    assert response.status_code == 200


def test_post(app, client):
    # POST /coach/
    response = post(app, client)
    coach_id = json.loads(response.get_data())
    assert validate_uuid(coach_id, 4) is True  # response must be a valid uuid4
    assert response.status_code == 201


def test_get_item(app, client, coach_id):
    # GET /coach/{id_}
    response = get_item(app, client, coach_id)
    setup_item = json.loads(response.get_data())
    assert setup_item["coach_id"] == coach_id
    assert validate_uuid(setup_item["coach_id"], 4) is True
    for key, value in default_payload_post.items():
        assert setup_item[key] == value
    assert response.status_code == 200


def test_put_item(app, client, coach_id):
    # PUT /coach/{id_}
    response = put_item(app, client, coach_id)
    assert response.status_code == 204

    response = get_item(app, client, coach_id)
    setup_item = json.loads(response.get_data())
    assert setup_item["coach_id"] == coach_id
    assert validate_uuid(setup_item["coach_id"], 4) is True
    for key, value in default_payload_put.items():
        assert setup_item[key] == value


def test_delete_item(app, client, coach_id):
    # DELETE /coach/{id_}
    response = delete_item(app, client, coach_id)
    assert response.status_code == 204

    response = None
    try:
        response = get_item(app, client, coach_id)
    except NoResultFound:
        assert response is None
