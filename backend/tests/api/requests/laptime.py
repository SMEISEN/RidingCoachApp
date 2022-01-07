import json
from datetime import datetime, timezone
from backend.tests.api.requests.session import post as post_session

default_payload_post = {
    "lap_no": 1,
    "valid": True,
    "laptime_seconds": 66.61,
    "sectors": {
        "Sector 1": 39.9,
        "Sector 2": 36.57
    },
    "datetime_display": datetime.now(tz=timezone.utc).timestamp()
}

default_payload_put = {
    "lap_no": 2,
    "valid": False,
    "laptime_seconds": 67.61,
    "sectors": {
        "Sector 1": 40.4,
        "Sector 2": 37.07
    },
    "datetime_display": datetime.now(tz=timezone.utc).timestamp() + 2000
}


def get(app, client):
    response = client.get("/api/laptime", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def post(app, client, payload=None):
    if payload is None:
        payload = default_payload_post

    # post a session first
    response = post_session(app, client)
    payload["session_id"] = json.loads(response.get_data())

    response = client.post("/api/laptime", data=json.dumps(payload), content_type='application/json',
                           headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})
    payload.pop("session_id")

    return response


def get_item(app, client, id_):
    response = client.get(f"/api/laptime/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def put_item(app, client, id_, payload=None):
    if payload is None:
        payload = default_payload_put
    response = client.put(f"/api/laptime/{id_}", data=json.dumps(payload), content_type='application/json',
                          headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def delete_item(app, client, id_):
    response = client.delete(f"/api/laptime/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response
