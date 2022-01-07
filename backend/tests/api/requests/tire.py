import json
from backend.tests.api.requests.bike import post as post_bike

default_payload_post = {
    "active": False,
    "rim": "Alpina black",
    "category": "slick",
    "manufacturer": "Metzeler",
    "name": "Metzeler",
    "compound": "K1",
    "axis": "front",
    "dimension": "125/75R420",
    "dot": "1521",
    "condition": {
        "left_outer": 1,
        "left_middle": 1,
        "center": 1,
        "right_middle": 1,
        "right_outer": 1
    },
    "operating_hours": 0,
    "comment": "comment on the tire"
}

default_payload_put = {
    "active": True,
    "rim": "Alpina white",
    "category": "rain",
    "manufacturer": "Michelin",
    "name": "Michelin",
    "compound": "B2",
    "axis": "rear",
    "dimension": "160/60R17",
    "dot": "1621",
    "condition": {
        "left_outer": 0.95,
        "left_middle": 0.94,
        "center": 0.93,
        "right_middle": 0.92,
        "right_outer": 0.91
    },
    "operating_hours": 1.2,
    "comment": "comment"
}

def get(app, client):
    response = client.get("/api/tire", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def post(app, client, payload=None):
    if payload is None:
        payload = default_payload_post

    # post a bike first
    response = post_bike(app, client)
    payload["bike_id"] = json.loads(response.get_data())

    response = client.post("/api/tire", data=json.dumps(payload), content_type='application/json',
                           headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})
    payload.pop("bike_id")

    return response


def get_item(app, client, id_):
    response = client.get(f"/api/tire/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def put_item(app, client, id_, payload=None):
    if payload is None:
        payload = default_payload_put
    response = client.put(f"/api/tire/{id_}", data=json.dumps(payload), content_type='application/json',
                          headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def delete_item(app, client, id_):
    response = client.delete(f"/api/tire/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response
