import json
import pytest
from datetime import datetime
from backend.app import create_app
from backend.config import TestConfig
from backend.app import db
from backend.utils.uuid import validate_uuid

from backend.tests.api.requests.history import get
from backend.tests.api.requests.history import post
from backend.tests.api.requests.history import get_item
from backend.tests.api.requests.history import put_item
from backend.tests.api.requests.history import delete_item
from backend.tests.api.requests.history import post_query
from backend.tests.api.requests.history import default_payload_post, default_payload_put


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
def history_id(app, client):
    response = get(app, client)

    if bool(json.loads(response.get_data())) is False:
        # create a new history item
        response = post(app, client)
        history_id_ = json.loads(response.get_data())
    else:
        # extract id from existing history item
        history_id_ = response.get_data()[0]["history_id"]
    return history_id_


def test_get(app, client):
    # GET /history/
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty
    assert response.status_code == 200


def test_post(app, client):
    # POST /history/
    response = post(app, client)
    history_id = json.loads(response.get_data())
    assert validate_uuid(history_id, 4) is True  # response must be a valid uuid4
    assert response.status_code == 201


def test_get_item(app, client, history_id):
    # GET /history/{id_}
    response = get_item(app, client, history_id)
    history_item = json.loads(response.get_data())
    assert history_item["history_id"] == history_id
    assert validate_uuid(history_item["maintenance_id"], 4) is True
    assert validate_uuid(history_item["bike_id"], 4) is True
    for key, value in default_payload_post.items():
        if key == "datetime_display":
            assert history_item[key] == datetime.utcfromtimestamp(value).isoformat()  # this should be unified
        else:
            assert history_item[key] == value
    assert response.status_code == 200


def test_put_item(app, client, history_id):
    # PUT /history/{id_}
    response = put_item(app, client, history_id)
    assert response.status_code == 204

    response = get_item(app, client, history_id)
    history_item = json.loads(response.get_data())
    assert history_item["history_id"] == history_id
    assert validate_uuid(history_item["history_id"], 4) is True
    assert validate_uuid(history_item["bike_id"], 4) is True
    for key, value in default_payload_put.items():
        if key == "datetime_display":
            assert history_item[key] == datetime.utcfromtimestamp(value).isoformat()  # this should be unified
        else:
            assert history_item[key] == value


def test_delete_item(app, client, history_id):
    # DELETE /history/{id_}
    response = delete_item(app, client, history_id)
    assert response.status_code == 204
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty


def test_post_query(app, client):
    # POST /history/query
    response = post_query(app, client)
    assert response.status_code == 200

    # post new default item
    post(app, client)

    payload = {
        "active": "false",
    }
    response = post_query(app, client, payload)
    history_items = json.loads(response.get_data())
    assert isinstance(history_items, list)
    assert len(history_items) == 1
    history_item = history_items[0]
    for key, value in default_payload_post.items():
        if key == "datetime_display":
            assert history_item[key] == datetime.utcfromtimestamp(value).isoformat()  # this should be unified
        else:
            assert history_item[key] == value
    assert response.status_code == 200

    payload = {
        "category": "slick",
    }
    response = post_query(app, client, payload)
    history_items = json.loads(response.get_data())
    assert isinstance(history_items, list)
    assert len(history_items) == 1
    history_item = history_items[0]
    for key, value in default_payload_post.items():
        if key == "datetime_display":
            assert history_item[key] == datetime.utcfromtimestamp(value).isoformat()  # this should be unified
        else:
            assert history_item[key] == value
    assert response.status_code == 200

    payload = {
        "axis": "front",
    }
    response = post_query(app, client, payload)
    history_items = json.loads(response.get_data())
    assert isinstance(history_items, list)
    assert len(history_items) == 1
    history_item = history_items[0]
    for key, value in default_payload_post.items():
        if key == "datetime_display":
            assert history_item[key] == datetime.utcfromtimestamp(value).isoformat()  # this should be unified
        else:
            assert history_item[key] == value
    assert response.status_code == 200

    payload = {
        "operating_hours": {
            "values": [
                66,
                99.6
            ],
            "operators": [
                ">=",
                "<="
            ]
        },
    }
    response = post_query(app, client, payload)
    history_items = json.loads(response.get_data())
    for history_item in history_items:
        assert payload["operating_hours"]["values"][0] <= history_item["operating_hours"]
        assert payload["operating_hours"]["values"][1] >= history_item["operating_hours"]
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
    history_items = json.loads(response.get_data())
    for history_item in history_items:
        assert history_item["datetime_display"] >= datetime.utcfromtimestamp(
            payload["datetime_display"]["values"][0]).isoformat()
        assert history_item["datetime_display"] <= datetime.utcfromtimestamp(
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
    history_items = json.loads(response.get_data())
    for history_item in history_items:
        assert history_item["datetime_created"] >= datetime.utcfromtimestamp(
            payload["datetime_created"]["values"][0]).isoformat()
        assert history_item["datetime_created"] <= datetime.utcfromtimestamp(
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
    history_items = json.loads(response.get_data())
    for history_item in history_items:
        assert history_item["datetime_last_modified"] >= datetime.utcfromtimestamp(
            payload["datetime_last_modified"]["values"][0]).isoformat()
        assert history_item["datetime_last_modified"] <= datetime.utcfromtimestamp(
            payload["datetime_last_modified"]["values"][1]).isoformat()
    assert response.status_code == 200
