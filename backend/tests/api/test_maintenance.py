import json
import pytest
from sqlalchemy.orm.exc import NoResultFound
from backend.app import create_app
from backend.config import TestConfig
from backend.app import db
from backend.utils.uuid import validate_uuid
from backend.tests.api.routines.query import validate_filter_by, validate_filter_intervals

from backend.tests.api.requests.maintenance import get
from backend.tests.api.requests.maintenance import post
from backend.tests.api.requests.maintenance import get_item
from backend.tests.api.requests.maintenance import put_item
from backend.tests.api.requests.maintenance import delete_item
from backend.tests.api.requests.maintenance import post_query
from backend.tests.api.requests.maintenance import get_warnings
from backend.tests.api.requests.maintenance import default_payload_post, default_payload_put
from backend.tests.api.requests.history import post as post_history
from backend.tests.api.requests.history import get_item as get_history_item


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
def maintenance_id(app, client):
    # create a new maintenance item
    response = post(app, client)
    _maintenance_id = json.loads(response.get_data())

    return _maintenance_id


def test_get(app, client):
    # GET /maintenance/
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty
    assert response.status_code == 200

    # post two maintenance items
    post(app, client, default_payload_post)
    post(app, client, default_payload_put)

    response = get(app, client)
    maintenance_items = json.loads(response.get_data())
    assert isinstance(maintenance_items, list)
    assert len(maintenance_items) == 2
    assert response.status_code == 200


def test_post(app, client):
    # POST /maintenance/
    response = post(app, client)
    maintenance_id = json.loads(response.get_data())
    assert validate_uuid(maintenance_id, 4) is True  # response must be a valid uuid4
    assert response.status_code == 201


def test_get_item(app, client, maintenance_id):
    # GET /maintenance/{id_}
    response = get_item(app, client, maintenance_id)
    maintenance_item = json.loads(response.get_data())
    assert maintenance_item["maintenance_id"] == maintenance_id
    assert validate_uuid(maintenance_item["maintenance_id"], 4) is True
    assert validate_uuid(maintenance_item["bike_id"], 4) is True
    for key, value in default_payload_post.items():
        assert maintenance_item[key] == value
    assert response.status_code == 200


def test_put_item(app, client, maintenance_id):
    # PUT /maintenance/{id_}
    response = put_item(app, client, maintenance_id)
    assert response.status_code == 204

    response = get_item(app, client, maintenance_id)
    maintenance_item = json.loads(response.get_data())
    assert maintenance_item["maintenance_id"] == maintenance_id
    assert validate_uuid(maintenance_item["maintenance_id"], 4) is True
    assert validate_uuid(maintenance_item["bike_id"], 4) is True
    for key, value in default_payload_put.items():
        assert maintenance_item[key] == value


def test_delete_item(app, client, maintenance_id):
    # DELETE /maintenance/{id_}
    response = delete_item(app, client, maintenance_id)
    assert response.status_code == 204

    response = None
    try:
        response = get_item(app, client, maintenance_id)
    except NoResultFound:
        assert response is None


def test_post_query(app, client, maintenance_id):
    # POST /maintenance/query
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

    def validate_tags_default(payload):
        response = post_query(app, client, payload)
        items = json.loads(response.get_data())
        assert isinstance(items, list)
        for item in items:
            for key, value in payload.items():
                assert any(tag in item[key] for tag in payload[key]) is True
        assert response.status_code == 200
    validate_tags_default({"tags_default": ["checked", "fixed", "replaced"]})
    validate_tags_default({"tags_default": ["checked"]})

    validate_filter_by(payload={"bike_id": bike_id_post}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"bike_id": bike_id_put}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"interval_unit": "h"}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"interval_unit": "a"}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"interval_type": "planned cycle"}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"interval_type": "estimated wear"}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"name": "maintenance name"}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"name": "name maintenance"}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"category": "maintenance category"}, post_query=post_query, app=app, client=client)
    validate_filter_by(payload={"category": "category maintenance"}, post_query=post_query, app=app, client=client)

    validate_filter_intervals(payload={
            "interval_amount": {
                "values": [
                    9,
                    11
                ],
                "operators": [
                    ">=",
                    "<="
                ]
            },
        }, post_query=post_query, app=app, client=client)


def test_get_warnings(app, client):
    # GET /maintenance/warnings

    # post maintenance and history item
    response = post_history(app, client)

    # get bike_id
    response = get_history_item(app, client, json.loads(response.get_data()))

    response = get_warnings(app, client, json.loads(response.get_data())["bike_id"])
    warning_data = json.loads(response.get_data())
    assert isinstance(warning_data, dict)
    assert isinstance(warning_data["warnings"], int)
    assert isinstance(warning_data["overdue_maintenance"], list)

    for sparepart in warning_data["overdue_maintenance"]:
        for key in default_payload_post.keys():
            assert (key in list(sparepart.keys())) is True
