import json
import pytest
from backend.app import create_app
from backend.config import TestConfig
from backend.app import db
from backend.utils.uuid import validate_uuid

from backend.tests.api.requests.tire import get
from backend.tests.api.requests.tire import post
from backend.tests.api.requests.tire import get_item
from backend.tests.api.requests.tire import put_item
from backend.tests.api.requests.tire import delete_item
from backend.tests.api.requests.tire import default_payload_post, default_payload_put


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
def tire_id(app, client):
    response = get(app, client)

    if bool(json.loads(response.get_data())) is False:
        # create a new tire item
        response = post(app, client)
        _tire_id = json.loads(response.get_data())
    else:
        # extract id from existing tire item
        _tire_id = response.get_data()[0]["tire_id"]
    return _tire_id


def test_get(app, client):
    # GET /tire/
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty
    assert response.status_code == 200

    # post two tire items
    post(app, client, default_payload_post)
    post(app, client, default_payload_put)

    response = get(app, client)
    tire_items = json.loads(response.get_data())
    assert isinstance(tire_items, list)
    assert len(tire_items) == 2
    assert response.status_code == 200


def test_post(app, client):
    # POST /tire/
    response = post(app, client)
    tire_id = json.loads(response.get_data())
    assert validate_uuid(tire_id, 4) is True  # response must be a valid uuid4
    assert response.status_code == 201


def test_get_item(app, client, tire_id):
    # GET /tire/{id_}
    response = get_item(app, client, tire_id)
    tire_item = json.loads(response.get_data())
    assert tire_item["tire_id"] == tire_id
    assert validate_uuid(tire_item["tire_id"], 4) is True
    for key, value in default_payload_post.items():
        assert tire_item[key] == value
    assert response.status_code == 200


def test_put_item(app, client, tire_id):
    # PUT /tire/{id_}
    response = put_item(app, client, tire_id)
    assert response.status_code == 204

    response = get_item(app, client, tire_id)
    tire_item = json.loads(response.get_data())
    assert tire_item["tire_id"] == tire_id
    assert validate_uuid(tire_item["tire_id"], 4) is True
    for key, value in default_payload_put.items():
        assert tire_item[key] == value


def test_delete_item(app, client, tire_id):
    # DELETE /tire/{id_}
    response = delete_item(app, client, tire_id)
    assert response.status_code == 204
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty

def test_post_query():
    # tbd
    # todo: post two bikes, then get, must be 2, must be a list
    pass
