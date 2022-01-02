import json
import pytest
from datetime import datetime
from backend.app import create_app
from backend.config import TestConfig
from backend.app import db
from backend.utils.uuid import validate_uuid

from backend.tests.api.requests.training import get
from backend.tests.api.requests.training import post
from backend.tests.api.requests.training import get_item
from backend.tests.api.requests.training import put_item
from backend.tests.api.requests.training import delete_item
from backend.tests.api.requests.training import post_query
from backend.tests.api.requests.training import default_payload_post, default_payload_put


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
def training_id(app, client):
    response = get(app, client)

    if bool(json.loads(response.get_data())) is False:
        # create a new training item
        response = post(app, client)
        _training_id = json.loads(response.get_data())
    else:
        # extract id from existing training item
        _training_id = response.get_data()[0]["training_id"]
    return _training_id


@pytest.fixture
def client(app):
    _client = app.test_client()
    return _client


def test_get(app, client):
    # GET /training/
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty
    assert response.status_code == 200


def test_post(app, client):
    # POST /training/
    response = post(app, client)
    training_id = json.loads(response.get_data())
    assert validate_uuid(training_id, 4) is True  # response must be a valid uuid4
    assert response.status_code == 201


def test_get_item(app, client, training_id):
    # GET /training/{id_}
    response = get_item(app, client, training_id)
    training_item = json.loads(response.get_data())
    assert training_item["training_id"] == training_id
    assert validate_uuid(training_item["training_id"], 4) is True
    for key, value in default_payload_post.items():
        if key == "datetime_display":
            assert training_item[key] == datetime.utcfromtimestamp(value).isoformat()  # this should be unified
        else:
            assert training_item[key] == value
    assert response.status_code == 200


def test_put_item(app, client, training_id):
    # PUT /training/{id_}
    response = put_item(app, client, training_id)
    assert response.status_code == 204

    response = get_item(app, client, training_id)
    training_item = json.loads(response.get_data())
    assert training_item["training_id"] == training_id
    assert validate_uuid(training_item["training_id"], 4) is True
    for key, value in default_payload_put.items():
        if key == "datetime_display":
            assert training_item[key] == datetime.utcfromtimestamp(value).isoformat()  # this should be unified
        else:
            assert training_item[key] == value


def test_delete_item(app, client, training_id):
    # DELETE /training/{id_}
    response = delete_item(app, client, training_id)
    assert response.status_code == 204
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty


def test_post_query(app, client):
    # POST /training/query
    response = post_query(app, client)
    assert response.status_code == 200

    # post new default item
    post(app, client)

    payload = {
        "location": "track name",
    }
    response = post_query(app, client, payload)
    training_items = json.loads(response.get_data())
    assert isinstance(training_items, list)
    assert len(training_items) == 1
    training_item = training_items[0]
    for key, value in default_payload_post.items():
        if key == "datetime_display":
            assert training_item[key] == datetime.utcfromtimestamp(value).isoformat()  # this should be unified
        else:
            assert training_item[key] == value
    assert response.status_code == 200

    payload = {
        "datetime_display": {
            "values": [
                datetime.utcnow().timestamp() - 2000,
                datetime.utcnow().timestamp(),
                ],
            "operators": [
                ">=",
                "<="
            ]
        },
    }
    response = post_query(app, client, payload)
    training_items = json.loads(response.get_data())
    for training_item in training_items:
        assert training_item["datetime_display"] >= datetime.utcfromtimestamp(
            payload["datetime_display"]["values"][0]).isoformat()
        assert training_item["datetime_display"] <= datetime.utcfromtimestamp(
            payload["datetime_display"]["values"][1]).isoformat()
    assert response.status_code == 200

    payload = {
        "datetime_created": {
            "values": [
                datetime.utcnow().timestamp() - 2000,
                datetime.utcnow().timestamp(),
                ],
            "operators": [
                ">=",
                "<="
            ]
        },
    }
    response = post_query(app, client, payload)
    training_items = json.loads(response.get_data())
    for training_item in training_items:
        assert training_item["datetime_created"] >= datetime.utcfromtimestamp(
            payload["datetime_created"]["values"][0]).isoformat()
        assert training_item["datetime_created"] <= datetime.utcfromtimestamp(
            payload["datetime_created"]["values"][1]).isoformat()
    assert response.status_code == 200

    payload = {
        "datetime_last_modified": {
            "values": [
                datetime.utcnow().timestamp() - 2000,
                datetime.utcnow().timestamp(),
                ],
            "operators": [
                ">=",
                "<="
            ]
        },
    }
    response = post_query(app, client, payload)
    training_items = json.loads(response.get_data())
    for training_item in training_items:
        assert training_item["datetime_last_modified"] >= datetime.utcfromtimestamp(
            payload["datetime_last_modified"]["values"][0]).isoformat()
        assert training_item["datetime_last_modified"] <= datetime.utcfromtimestamp(
            payload["datetime_last_modified"]["values"][1]).isoformat()
    assert response.status_code == 200
