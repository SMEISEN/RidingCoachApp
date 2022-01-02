import json
from datetime import datetime
from backend.tests.api.requests.training import post as post_training
from backend.tests.api.requests.bike import post as post_bike

default_payload_post = {
    "operating_hours": 66.1,
    "weather_current": {
        "lat": 49.2966279,
        "lon": 8.601037,
        "temp": {
            "value": 30.04,
            "units": "C"
        },
        "type": "measurement"
    },
    "slick_pressure_front": 2,
    "slick_pressure_rear": 2,
    "rain_pressure_front": 2,
    "rain_pressure_rear": 2,
    "setup": [
        {
            "category": "Engine",
            "group": None,
            "name": "Power Mode",
            "ticks_available": 1,
            "ticks_current": 1,
            "ticks_standard": 1
        },
        {
            "category": "Suspension",
            "group": "Fork",
            "name": "Compression",
            "ticks_available": 37,
            "ticks_current": 14,
            "ticks_standard": 15
        }
    ],
    "comment": "comment",
    "datetime_display": datetime.utcnow().timestamp() + 2000
}

default_payload_put = {
    "operating_hours": 67.1,
    "weather_current": {
        "lat": 49.0,
        "lon": 8.7,
        "temp": {
            "value": 293,
            "units": "K"
        },
        "type": "measurement"
    },
    "slick_pressure_front": 1.9,
    "slick_pressure_rear": 1.8,
    "rain_pressure_front": 1.7,
    "rain_pressure_rear": 1.6,
    "setup": [
        {
            "category": "Engine",
            "group": None,
            "name": "Pwr Mode",
            "ticks_available": 2,
            "ticks_current": 2,
            "ticks_standard": 2
        },
        {
            "category": "Suspension",
            "group": "Shock",
            "name": "Rebound",
            "ticks_available": 35,
            "ticks_current": 13,
            "ticks_standard": 14
        }
    ],
    "comment": "cmt",
    "datetime_display": datetime.utcnow().timestamp()
}


def get(app, client):
    response = client.get("/api/setup", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

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

    response = client.post("/api/setup", data=json.dumps(payload), content_type='application/json',
                           headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def get_item(app, client, id_):
    response = client.get(f"/api/setup/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def put_item(app, client, id_, payload=None):
    if payload is None:
        payload = default_payload_put
    response = client.put(f"/api/setup/{id_}", data=json.dumps(payload), content_type='application/json',
                          headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def delete_item(app, client, id_):
    response = client.delete(f"/api/setup/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response
