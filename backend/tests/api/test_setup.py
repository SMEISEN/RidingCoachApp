import json
import pytest
from datetime import datetime
from backend.app import create_app
from backend.config import TestConfig
from backend.app import db
from backend.utils.uuid import validate_uuid

from backend.tests.api.requests.setup import get
from backend.tests.api.requests.setup import post
from backend.tests.api.requests.setup import get_item
from backend.tests.api.requests.setup import put_item
from backend.tests.api.requests.setup import delete_item
from backend.tests.api.requests.setup import default_payload_post, default_payload_put


@pytest.fixture
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


@pytest.fixture
def client(app):
    _client = app.test_client()
    return _client


@pytest.fixture
def setup_id(app, client):
    response = get(app, client)

    if bool(json.loads(response.get_data())) is False:
        # create a new setup item
        response = post(app, client)
        setup_id_ = json.loads(response.get_data())
    else:
        # extract id from existing setup item
        setup_id_ = response.get_data()[0]["setup_id"]
    return setup_id_


def test_get(app, client):
    # GET /setup/
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty
    assert response.status_code == 200


def test_post(app, client):
    # POST /setup/
    response = post(app, client)
    setup_id = json.loads(response.get_data())
    assert validate_uuid(setup_id, 4) is True  # response must be a valid uuid4
    assert response.status_code == 201


def test_get_item(app, client, setup_id):
    # GET /setup/{id_}
    response = get_item(app, client, setup_id)
    setup_item = json.loads(response.get_data())
    assert setup_item["setup_id"] == setup_id
    assert validate_uuid(setup_item["setup_id"], 4) is True
    for key, value in default_payload_post.items():
        if key == "datetime_display":
            assert setup_item[key] == datetime.utcfromtimestamp(value).isoformat()  # this should be unified
        else:
            assert setup_item[key] == value
    assert response.status_code == 200


def test_put_item(app, client, setup_id):
    # PUT /setup/{id_}
    response = put_item(app, client, setup_id)
    assert response.status_code == 204

    response = get_item(app, client, setup_id)
    setup_item = json.loads(response.get_data())
    assert setup_item["setup_id"] == setup_id
    assert validate_uuid(setup_item["setup_id"], 4) is True
    for key, value in default_payload_put.items():
        if key == "datetime_display":
            assert setup_item[key] == datetime.utcfromtimestamp(value).isoformat()  # this should be unified
        else:
            assert setup_item[key] == value


def test_delete_item(app, client, setup_id):
    # DELETE /setup/{id_}
    response = delete_item(app, client, setup_id)
    assert response.status_code == 204
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty
