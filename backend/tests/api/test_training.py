import json
import pytest
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, timezone
from backend.app import create_app
from backend.config import TestConfig
from backend.app import db
from backend.utils.uuid import validate_uuid
from backend.tests.api.routines.query import validate_filter_by, validate_filter_intervals

from backend.tests.api.requests.training import get
from backend.tests.api.requests.training import post
from backend.tests.api.requests.training import get_item
from backend.tests.api.requests.training import put_item
from backend.tests.api.requests.training import delete_item
from backend.tests.api.requests.training import post_query
from backend.tests.api.requests.training import default_payload_post, default_payload_put


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


@pytest.fixture(scope='function')  # each test needs to create its own item(scope='module')
def training_id(app, client):
    # create a new training item
    response = post(app, client)
    _training_id = json.loads(response.get_data())

    return _training_id


def test_get(app, client):
    # GET /training/
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty
    assert response.status_code == 200

    # post two training items
    post(app, client, default_payload_post)
    post(app, client, default_payload_put)

    response = get(app, client)
    training_items = json.loads(response.get_data())
    assert isinstance(training_items, list)
    assert len(training_items) == 2
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
            assert training_item[key] == datetime.fromtimestamp(value, tz=timezone.utc).replace(tzinfo=None)\
                .isoformat()  # this should be unified
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
            assert training_item[key] == datetime.fromtimestamp(value, tz=timezone.utc).replace(tzinfo=None)\
                .isoformat()  # this should be unified
        else:
            assert training_item[key] == value


def test_delete_item(app, client, training_id):
    # DELETE /training/{id_}
    response = delete_item(app, client, training_id)
    assert response.status_code == 204

    response = None
    try:
        response = get_item(app, client, training_id)
    except NoResultFound:
        assert response is None


def test_post_query(app, client):
    # POST /training/query
    response = post_query(app, client)
    assert response.status_code == 200

    # post new default item
    post(app, client, default_payload_post)
    post(app, client, default_payload_put)

    # query invalid parameter
    payload = {
        "test314": "test314",
    }
    response = post_query(app, client, payload)
    assert len(json.loads(response.get_data())) == 0
    assert response.status_code == 404

    # query single keys
    validate_filter_by(payload={"location": "track name"}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"location": "name track"}, post_query=post_query, app=app, client=client)

    # query intervals
    validate_filter_intervals(payload={
        "datetime_display": {
            "values": [
                datetime.now(tz=timezone.utc).timestamp() - 2000,
                datetime.now(tz=timezone.utc).timestamp(),
                ],
            "operators": [
                ">=",
                "<="
            ]
        },
    }, post_query=post_query, app=app, client=client)
    validate_filter_intervals(payload={
        "datetime_created": {
            "values": [
                datetime.now(tz=timezone.utc).timestamp() - 2000,
                datetime.now(tz=timezone.utc).timestamp(),
                ],
            "operators": [
                ">=",
                "<="
            ]
        },
    }, post_query=post_query, app=app, client=client)
    validate_filter_intervals(payload={
        "datetime_last_modified": {
            "values": [
                datetime.now(tz=timezone.utc).timestamp() - 2000,
                datetime.now(tz=timezone.utc).timestamp(),
                ],
            "operators": [
                ">=",
                "<="
            ]
        },
    }, post_query=post_query, app=app, client=client)
