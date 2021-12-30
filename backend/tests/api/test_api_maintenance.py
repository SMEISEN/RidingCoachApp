import json
from backend.app import create_app
from backend.config import TestConfig
from backend.app import db
from backend.utils.uuid import validate_uuid

from backend.tests.api.requests.maintenance import get
from backend.tests.api.requests.maintenance import post
from backend.tests.api.requests.maintenance import get_item
from backend.tests.api.requests.maintenance import put_item
from backend.tests.api.requests.maintenance import delete_item
from backend.tests.api.requests.maintenance import post_query
from backend.tests.api.requests.maintenance import default_payload_post, default_payload_put


def test_api_maintenance():
    app = create_app(TestConfig)

    # create test tables
    with app.app_context():
        db.drop_all()
        db.create_all()

    # setup client
    client = app.test_client()

    # test requests

    # GET /maintenance/
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty
    assert response.status_code == 200

    # POST /maintenance/
    response = post(app, client)
    maintenance_id = json.loads(response.get_data())
    assert validate_uuid(maintenance_id, 4) is True  # response must be a valid uuid4
    assert response.status_code == 201

    # GET /maintenance/{id_}
    response = get_item(app, client, maintenance_id)
    maintenance_item = json.loads(response.get_data())
    assert maintenance_item["maintenance_id"] == maintenance_id
    assert validate_uuid(maintenance_item["maintenance_id"], 4) is True
    assert validate_uuid(maintenance_item["bike_id"], 4) is True
    for key, value in default_payload_post.items():
        assert maintenance_item[key] == value
    assert response.status_code == 200

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

    # DELETE /maintenance/{id_}
    response = delete_item(app, client, maintenance_id)
    assert response.status_code == 204
    response = get(app, client)
    assert bool(json.loads(response.get_data())) is False  # response must be empty

    # POST /maintenance/query
    response = post_query(app, client)
    assert response.status_code == 200

    post(app, client)  # post new default item

    payload = {
        "category": "maintenance category",
    }
    response = post_query(app, client, payload)
    maintenance_items = json.loads(response.get_data())
    for key in maintenance_items.keys():
        assert key == payload["category"]
    assert response.status_code == 200

    payload = {
        "name": "maintenance name",
    }
    response = post_query(app, client, payload)
    maintenance_items = json.loads(response.get_data())
    for value in maintenance_items.values():
        for key in value.keys():
            assert key == payload["name"]
    assert response.status_code == 200

    payload = {
        "interval_unit": "h",
    }
    response = post_query(app, client, payload)
    maintenance_items = json.loads(response.get_data())
    for value in maintenance_items.values():
        for value_value in value.values():
            assert value_value["interval_unit"] == payload["interval_unit"]
    assert response.status_code == 200

    payload = {
        "interval_type": "planned cycle",
    }
    response = post_query(app, client, payload)
    maintenance_items = json.loads(response.get_data())
    for value in maintenance_items.values():
        for value_value in value.values():
            assert value_value["interval_type"] == payload["interval_type"]
    assert response.status_code == 200

    payload = {
        "tags_default": [
            "checked",
            "fixed",
            "replaced"
        ]
    }
    response = post_query(app, client, payload)
    maintenance_items = json.loads(response.get_data())
    for value in maintenance_items.values():
        for value_value in value.values():
            assert value_value["tags_default"] == payload["tags_default"]
    assert response.status_code == 200

    payload = {
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
    }
    response = post_query(app, client, payload)
    maintenance_items = json.loads(response.get_data())
    for value in maintenance_items.values():
        for valuevalue in value.values():
            assert payload["interval_amount"]["values"][0] <= valuevalue["interval_amount"]
            assert payload["interval_amount"]["values"][1] >= valuevalue["interval_amount"]
    assert response.status_code == 200

    # drop test tables
    with app.app_context():
        db.drop_all()
