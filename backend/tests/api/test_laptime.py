import json
import pytest
from datetime import datetime, timezone
from backend.app import create_app
from backend.config import TestConfig
from backend.app import db
from backend.utils.uuid import validate_uuid

from backend.tests.api.requests.laptime import get
from backend.tests.api.requests.laptime import post
from backend.tests.api.requests.laptime import get_item
from backend.tests.api.requests.laptime import put_item
from backend.tests.api.requests.laptime import delete_item
from backend.tests.api.requests.laptime import default_payload_post, default_payload_put


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
def lap_id(app, client):
    response = get(app, client)

    if bool(json.loads(response.get_data())) is False:
        # create a new laptime item
        response = post(app, client)
        _lap_id = json.loads(response.get_data())
    else:
        # extract id from existing laptime item
        _lap_id = response.get_data()[0]["lap_id"]
    return _lap_id


def test_get(app, client):
    # GET /laptime/
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty
    assert response.status_code == 200

    # post two laptime items
    post(app, client, default_payload_post)
    post(app, client, default_payload_put)

    response = get(app, client)
    laptime_items = json.loads(response.get_data())
    assert isinstance(laptime_items, list)
    assert len(laptime_items) == 2
    assert response.status_code == 200


def test_post(app, client):
    # POST /laptime/
    response = post(app, client)
    lap_id = json.loads(response.get_data())
    assert validate_uuid(lap_id, 4) is True  # response must be a valid uuid4
    assert response.status_code == 201


def test_get_item(app, client, lap_id):
    # GET /laptime/{id_}
    response = get_item(app, client, lap_id)
    laptime_item = json.loads(response.get_data())
    assert laptime_item["lap_id"] == lap_id
    assert validate_uuid(laptime_item["lap_id"], 4) is True
    for key, value in default_payload_post.items():
        if key == "datetime_display":
            assert laptime_item[key] == datetime.fromtimestamp(value, tz=timezone.utc).replace(tzinfo=None)\
                .isoformat()  # this should be unified
        else:
            assert laptime_item[key] == value
    assert response.status_code == 200


def test_put_item(app, client, lap_id):
    # PUT /laptime/{id_}
    response = put_item(app, client, lap_id)
    assert response.status_code == 204

    response = get_item(app, client, lap_id)
    laptime_item = json.loads(response.get_data())
    assert laptime_item["lap_id"] == lap_id
    assert validate_uuid(laptime_item["lap_id"], 4) is True
    for key, value in default_payload_put.items():
        if key == "datetime_display":
            assert laptime_item[key] == datetime.fromtimestamp(value, tz=timezone.utc).replace(tzinfo=None)\
                .isoformat()  # this should be unified
        else:
            assert laptime_item[key] == value


def test_delete_item(app, client, lap_id):
    # DELETE /laptime/{id_}
    response = delete_item(app, client, lap_id)
    assert response.status_code == 204
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty
