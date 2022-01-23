import json
import pytest
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, timezone
from backend.app import create_app
from backend.config import TestConfig
from backend.app import db
from backend.utils.uuid import validate_uuid

from backend.tests.api.requests.session import get
from backend.tests.api.requests.session import post
from backend.tests.api.requests.session import get_item
from backend.tests.api.requests.session import put_item
from backend.tests.api.requests.session import delete_item
from backend.tests.api.requests.session import default_payload_post, default_payload_put


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
def session_id(app, client):
    # create a new session item
    response = post(app, client)
    _session_id = json.loads(response.get_data())

    return _session_id


def test_get(app, client):
    # GET /session/
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty
    assert response.status_code == 200

    # post two session items
    post(app, client, default_payload_post)
    post(app, client, default_payload_put)

    response = get(app, client)
    session_items = json.loads(response.get_data())
    assert isinstance(session_items, list)
    assert len(session_items) == 2
    assert response.status_code == 200


def test_post(app, client):
    # POST /session/
    response = post(app, client)
    session_id = json.loads(response.get_data())
    assert validate_uuid(session_id, 4) is True  # response must be a valid uuid4
    assert response.status_code == 201


def test_get_item(app, client, session_id):
    # GET /session/{id_}
    response = get_item(app, client, session_id)
    session_item = json.loads(response.get_data())
    assert session_item["session_id"] == session_id
    assert validate_uuid(session_item["session_id"], 4) is True
    for key, value in default_payload_post.items():
        if key == "datetime_display":
            assert session_item[key] == datetime.fromtimestamp(value, tz=timezone.utc).replace(tzinfo=None)\
                .isoformat()  # this should be unified
        else:
            assert session_item[key] == value
    assert response.status_code == 200


def test_put_item(app, client, session_id):
    # PUT /session/{id_}
    response = put_item(app, client, session_id)
    assert response.status_code == 204

    response = get_item(app, client, session_id)
    session_item = json.loads(response.get_data())
    assert session_item["session_id"] == session_id
    assert validate_uuid(session_item["session_id"], 4) is True
    for key, value in default_payload_put.items():
        if key == "datetime_display":
            assert session_item[key] == datetime.fromtimestamp(value, tz=timezone.utc).replace(tzinfo=None)\
                .isoformat()  # this should be unified
        else:
            assert session_item[key] == value


def test_delete_item(app, client, session_id):
    # DELETE /session/{id_}
    response = delete_item(app, client, session_id)
    assert response.status_code == 204

    response = None
    try:
        response = get_item(app, client, session_id)
    except NoResultFound:
        assert response is None
