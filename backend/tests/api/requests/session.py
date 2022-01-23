import json
from datetime import datetime, timezone
from backend.tests.api.requests.training import post as post_training
from backend.tests.api.requests.bike import post as post_bike
from backend.tests.api.requests.setup import post as post_setup

default_payload_post = {
    "datetime_display": datetime.now(tz=timezone.utc).timestamp()
}

default_payload_put = {
    "datetime_display": datetime.now(tz=timezone.utc).timestamp() + 2000
}


def get(app, client):
    response = client.get("/api/session", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def post(app, client, payload=None):
    if payload is None:
        payload = default_payload_post

    # post a training first
    response = post_training(app, client)
    payload["training_id"] = json.loads(response.get_data())

    # post a bike first
    response = post_bike(app, client)
    payload["bike_id"] = json.loads(response.get_data())

    # post a setup first
    response = post_setup(app, client)
    payload["setup_id"] = json.loads(response.get_data())

    response = client.post("/api/session", data=json.dumps(payload), content_type='application/json',
                           headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})
    payload.pop("training_id")
    payload.pop("bike_id")
    payload.pop("setup_id")

    return response


def get_item(app, client, id_):
    response = client.get(f"/api/session/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def put_item(app, client, id_, payload=None):
    if payload is None:
        payload = default_payload_put
    response = client.put(f"/api/session/{id_}", data=json.dumps(payload), content_type='application/json',
                          headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def delete_item(app, client, id_):
    response = client.delete(f"/api/session/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response
