import json
import pytest
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, timezone
from backend.app import create_app
from backend.config import TestConfig
from backend.app import db
from backend.utils.uuid import validate_uuid
from backend.tests.api.routines.query import validate_filter_by, validate_filter_intervals

from backend.tests.api.requests.history import get
from backend.tests.api.requests.history import post
from backend.tests.api.requests.history import get_item
from backend.tests.api.requests.history import put_item
from backend.tests.api.requests.history import delete_item
from backend.tests.api.requests.history import post_query
from backend.tests.api.requests.history import default_payload_post, default_payload_put


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
def history_id(app, client):
    # create a new history item
    response = post(app, client)
    _history_id = json.loads(response.get_data())

    return _history_id


def test_get(app, client):
    # GET /history/
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty
    assert response.status_code == 200

    # post two history items
    post(app, client, default_payload_post)
    post(app, client, default_payload_put)

    response = get(app, client)
    history_items = json.loads(response.get_data())
    assert isinstance(history_items, list)
    assert len(history_items) == 2
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
            assert history_item[key] == datetime.fromtimestamp(value, tz=timezone.utc).replace(tzinfo=None)\
                .isoformat()  # this should be unified
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
            assert history_item[key] == datetime.fromtimestamp(value, tz=timezone.utc).replace(tzinfo=None)\
                .isoformat()  # this should be unified
        else:
            assert history_item[key] == value


def test_delete_item(app, client, history_id):
    # DELETE /history/{id_}
    response = delete_item(app, client, history_id)
    assert response.status_code == 204

    response = None
    try:
        response = get_item(app, client, history_id)
    except NoResultFound:
        assert response is None


def test_post_query(app, client):
    # POST /history/query
    response = post_query(app, client)
    assert response.status_code == 200

    # post new default item
    response = post(app, client, default_payload_post)
    response = get_item(app, client, json.loads(response.get_data()))
    bike_id_post = json.loads(response.get_data())["bike_id"]
    response = post(app, client, default_payload_put)
    response = get_item(app, client, json.loads(response.get_data()))
    bike_id_put = json.loads(response.get_data())["bike_id"]

    # query invalid parameter
    payload = {
        "test314": "test314",
    }
    response = post_query(app, client, payload)
    assert len(json.loads(response.get_data())) == 0
    assert response.status_code == 404

    # query single keys
    validate_filter_by(payload={"bike_id": bike_id_post}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"bike_id": bike_id_put}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={
        "comment": "comment on the maintenance entry"
    }, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={
        "comment": "comment on the updated maintenance entry"
    }, post_query=post_query, app=app, client=client)

    def validate_tags(payload):
        response = post_query(app, client, payload)
        items = json.loads(response.get_data())
        assert isinstance(items, list)
        for item in items:
            for key, value in payload.items():
                assert any(tag in item[key] for tag in payload[key]) is True
        assert response.status_code == 200
    validate_tags({"tags": ["checked", "fixed", "replaced"]})
    validate_tags({"tags": ["checked"]})

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
    validate_filter_intervals(payload={
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
    }, post_query=post_query, app=app, client=client)
