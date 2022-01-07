import json
import pytest
from datetime import datetime, timezone
from sqlalchemy.orm.exc import NoResultFound
from backend.app import create_app
from backend.config import TestConfig
from backend.app import db
from backend.utils.uuid import validate_uuid
from backend.tests.api.routines.query import validate_filter_by, validate_filter_intervals

from backend.tests.api.requests.tire import get
from backend.tests.api.requests.tire import post
from backend.tests.api.requests.tire import get_item
from backend.tests.api.requests.tire import put_item
from backend.tests.api.requests.tire import delete_item
from backend.tests.api.requests.tire import post_query
from backend.tests.api.requests.tire import default_payload_post, default_payload_put


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
def tire_id(app, client):
    # create a new tire item
    response = post(app, client)
    _tire_id = json.loads(response.get_data())

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

    response = None
    try:
        response = get_item(app, client, tire_id)
    except NoResultFound:
        assert response is None


def test_post_query(app, client, tire_id):
    # POST /tire/query
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
    validate_filter_by(payload={"active": True}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"active": False}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"category": "slick"}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"category": "rain"}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"axis": "front"}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"axis": "rear"}, post_query=post_query, app=app, client=client)

    # query intervals
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
    validate_filter_intervals(payload={
        "operating_hours": {
            "values": [0, 2],
            "operators": [
                ">=",
                "<="
            ]
        },
    }, post_query=post_query, app=app, client=client)
