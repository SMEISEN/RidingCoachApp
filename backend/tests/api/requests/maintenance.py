import json
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from backend.tests.api.requests.bike import post as post_bike

default_payload_post = {
    "category": "maintenance category",
    "name": "maintenance name",
    "interval_amount": 10,
    "interval_unit": "h",
    "interval_type": "planned cycle",
    "tags_default": [
        "checked",
        "fixed",
        "replaced"
    ]
}

default_payload_put = {
    "category": "category maintenance",
    "name": "name maintenance",
    "interval_amount": 1,
    "interval_unit": "a",
    "interval_type": "estimated wear",
    "tags_default": [
        "checked"
    ]
}

default_payload_query = {
    "category": "maintenance category",
    "name": "maintenance name",
    "interval_amount": {
        "values": [
            5,
            10
        ],
        "operators": [
            ">=",
            "<="
        ]
    },
    "interval_unit": "h",
    "interval_type": "planned cycle",
    "tags_default": [
        "checked",
        "fixed",
        "replaced"
    ]
}


def get(app, client):
    response = client.get("/api/maintenance", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def post(app, client, payload=None):
    if payload is None:
        payload = default_payload_post

    # post a bike first
    response = post_bike(app, client)
    payload["bike_id"] = json.loads(response.get_data())

    try:
        response = client.post("/api/maintenance", data=json.dumps(payload), content_type='application/json',
                               headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})
    except IntegrityError:
        # maintenance name already exists
        payload["name"] = payload["name"] + datetime.now().strftime("%m%d%Y%H%M%S")
        response = client.post("/api/maintenance", data=json.dumps(payload), content_type='application/json',
                               headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def get_item(app, client, id_):
    response = client.get(f"/api/maintenance/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def put_item(app, client, id_, payload=None):
    if payload is None:
        payload = default_payload_put
    response = client.put(f"/api/maintenance/{id_}", data=json.dumps(payload), content_type='application/json',
                          headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def delete_item(app, client, id_):
    response = client.delete(f"/api/maintenance/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def post_query(app, client, payload=None):
    if payload is None:
        payload = default_payload_query
    response = client.post("/api/maintenance/query", data=json.dumps(payload), content_type='application/json',
                           headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response
