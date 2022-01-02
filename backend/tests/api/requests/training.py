import json
from datetime import datetime

default_payload_post = {
    "location": "track name",
    "weather_hourly": [
        {
            "lat": 47.4325306,
            "lon": 6.7046713,
            "temp": {
                "value": 17.5,
                "units": "C"
            },
            "observation_time": {
                "value": "2020-08-22T07:00:00.000Z"
            },
            "type": "measurement"
        },
        {
            "lat": 47.4325306,
            "lon": 6.7046713,
            "temp": {
                "value": 23.49,
                "units": "C"
            },
            "observation_time": {
                "value": "2020-08-22T16:00:00.000Z"
            },
            "type": "forecast"
        }
    ],
    "datetime_display": datetime.utcnow().timestamp()
}

default_payload_put = {
    "location": "name track",
    "weather_hourly": [
        {
            "lat": 47.5,
            "lon": 6.8,
            "temp": {
                "value": 291,
                "units": "K"
            },
            "observation_time": {
                "value": "2020-08-22T08:00:00.000Z"
            },
            "type": "measurement"
        },
        {
            "lat": 47.6,
            "lon": 6.6,
            "temp": {
                "value": 293,
                "units": "K"
            },
            "observation_time": {
                "value": "2020-08-22T16:00:00.000Z"
            },
            "type": "forecast"
        }
    ],
    "datetime_display": datetime.utcnow().timestamp() + 2000
}

default_payload_query = {
    "location": "track name",
    "datetime_created": {
        "values": [
            datetime.utcnow().timestamp() - 2000,
            datetime.utcnow().timestamp(),
        ],
        "operators": [
            ">=",
            "<="
        ]
    },
    "datetime_last_modified": {
        "values": [
            datetime.utcnow().timestamp() - 2000,
            datetime.utcnow().timestamp(),
        ],
        "operators": [
            ">=",
            "<="
        ]
    },
    "datetime_display": {
        "values": [
            datetime.utcnow().timestamp() - 2000,
            datetime.utcnow().timestamp(),
        ],
        "operators": [
            ">=",
            "<="
        ]
    }
}


def get(app, client):
    response = client.get("/api/training", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def post(app, client, payload=None):
    if payload is None:
        payload = default_payload_post

    response = client.post("/api/training", data=json.dumps(payload), content_type='application/json',
                           headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def get_item(app, client, id_):
    response = client.get(f"/api/training/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def put_item(app, client, id_, payload=None):
    if payload is None:
        payload = default_payload_put
    response = client.put(f"/api/training/{id_}", data=json.dumps(payload), content_type='application/json',
                          headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def delete_item(app, client, id_):
    response = client.delete(f"/api/training/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def post_query(app, client, payload=None):
    if payload is None:
        payload = default_payload_query
    response = client.post("/api/training/query", data=json.dumps(payload), content_type='application/json',
                           headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response
