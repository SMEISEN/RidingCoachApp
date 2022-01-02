import json
import pytest
from backend.app import create_app
from backend.config import TestConfig
from backend.app import db
from backend.utils.uuid import validate_uuid

from backend.tests.api.requests.bike import get
from backend.tests.api.requests.bike import post
from backend.tests.api.requests.bike import get_item
from backend.tests.api.requests.bike import put_item
from backend.tests.api.requests.bike import delete_item
from backend.tests.api.requests.bike import default_payload_post, default_payload_put


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
def bike_id(app, client):
    response = get(app, client)

    if bool(json.loads(response.get_data())) is False:
        # create a new bike item
        response = post(app, client)
        _bike_id = json.loads(response.get_data())
    else:
        # extract id from existing bike item
        _bike_id = response.get_data()[0]["bike_id"]
    return _bike_id


def test_get(app, client):
    # GET /bike/
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty
    assert response.status_code == 200

    # post two bike items
    post(app, client, default_payload_post)
    post(app, client, default_payload_put)

    response = get(app, client)
    bike_items = json.loads(response.get_data())
    assert isinstance(bike_items, list)
    assert len(bike_items) == 2
    assert response.status_code == 200


def test_post(app, client):
    # POST /bike/
    response = post(app, client)
    bike_id = json.loads(response.get_data())
    assert validate_uuid(bike_id, 4) is True  # response must be a valid uuid4
    assert response.status_code == 201


def test_get_item(app, client, bike_id):
    # GET /bike/{id_}
    response = get_item(app, client, bike_id)
    bike_item = json.loads(response.get_data())
    assert bike_item["bike_id"] == bike_id
    assert validate_uuid(bike_item["bike_id"], 4) is True
    for key, value in default_payload_post.items():
        assert bike_item[key] == value
    assert response.status_code == 200


def test_put_item(app, client, bike_id):
    # PUT /bike/{id_}
    response = put_item(app, client, bike_id)
    assert response.status_code == 204

    response = get_item(app, client, bike_id)
    bike_item = json.loads(response.get_data())
    assert bike_item["bike_id"] == bike_id
    assert validate_uuid(bike_item["bike_id"], 4) is True
    for key, value in default_payload_put.items():
        assert bike_item[key] == value


def test_delete_item(app, client, bike_id):
    # DELETE /bike/{id_}
    response = delete_item(app, client, bike_id)
    assert response.status_code == 204
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty
