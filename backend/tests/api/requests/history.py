import json
from datetime import datetime, timezone
from backend.tests.api.requests.bike import post as post_bike
from backend.tests.api.requests.maintenance import post as post_maintenance

default_payload_post = {
    "operating_hours": 66.1,
    "comment": "comment on the maintenance entry",
    "tags": [
        "checked",
        "fixed",
        "replaced"
    ],
    "datetime_display": datetime.now(tz=timezone.utc).timestamp()
}

default_payload_put = {
    "operating_hours": 67.1,
    "comment": "comment on the updated maintenance entry",
    "tags": [
        "checked",
        "replaced"
    ],
    "datetime_display": datetime.now(tz=timezone.utc).timestamp() + 2000
}

default_payload_query = {
    "comment": "comment on the maintenance entry",
    "tags": [
        "checked",
        "fixed",
        "replaced"
    ],
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
    "datetime_last_modified": {
        "values": [
            datetime.now(tz=timezone.utc).timestamp() - 2000,
            datetime.now(tz=timezone.utc).timestamp(),
        ],
        "operators": [
            ">=",
            "<="
        ]
    }
}


def get(app, client):
    response = client.get("/api/history", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def post(app, client, payload=None):
    if payload is None:
        payload = default_payload_post

    # post a bike first
    response = post_bike(app, client)
    payload["bike_id"] = json.loads(response.get_data())

    # post a maintenance first
    response = post_maintenance(app, client)
    payload["maintenance_id"] = json.loads(response.get_data())

    response = client.post("/api/history", data=json.dumps(payload), content_type='application/json',
                           headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})
    payload.pop("bike_id")
    payload.pop("maintenance_id")

    return response


def get_item(app, client, id_):
    response = client.get(f"/api/history/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def put_item(app, client, id_, payload=None):
    if payload is None:
        payload = default_payload_put
    response = client.put(f"/api/history/{id_}", data=json.dumps(payload), content_type='application/json',
                          headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def delete_item(app, client, id_):
    response = client.delete(f"/api/history/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def post_query(app, client, payload=None):
    if payload is None:
        payload = default_payload_query
    response = client.post("/api/history/query", data=json.dumps(payload), content_type='application/json',
                           headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response
