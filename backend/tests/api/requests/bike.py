import json

default_payload_post = {
    "operating_hours": 66.1,
    "manufacturer": "manufacturer",
    "model": "model",
    "year": 2020,
    "ccm": 449.7,
    "stroke": 63,
    "piston": 97,
    "slick_front_name": "front slick name",
    "slick_front_notes": "front slick notes",
    "slick_front_pressure": [
        {
            "temperature": 40,
            "pressure": 1.7
        },
        {
            "temperature": 25,
            "pressure": 1.8
        }
    ],
    "slick_rear_name": "rear slick name",
    "slick_rear_notes": "rear slick notes",
    "slick_rear_pressure": [
        {
            "temperature": 40,
            "pressure": 1.7
        },
        {
            "temperature": 25,
            "pressure": 1.8
        }
    ],
    "rain_front_name": "front rain tire name",
    "rain_front_notes": "front rain tire notes",
    "rain_front_pressure": [
        {
            "temperature": 40,
            "pressure": 1.7
        },
        {
            "temperature": 25,
            "pressure": 1.8
        }
    ],
    "rain_rear_name": "rear rain tire name",
    "rain_rear_notes": "rear rain tire notes",
    "rain_rear_pressure": [
        {
            "temperature": 40,
            "pressure": 1.7
        },
        {
            "temperature": 25,
            "pressure": 1.8
        }
    ],
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
    ]
}

default_payload_put = {
    "operating_hours": 67.1,
    "manufacturer": "mftr",
    "model": "mdl",
    "year": 2021,
    "ccm": 450,
    "stroke": 65,
    "piston": 100,
    "slick_front_name": "front slick",
    "slick_front_notes": "front slick",
    "slick_front_pressure": [
        {
            "temperature": 39,
            "pressure": 1.8
        },
        {
            "temperature": 26,
            "pressure": 1.7
        }
    ],
    "slick_rear_name": "rear slick",
    "slick_rear_notes": "rear slick",
    "slick_rear_pressure": [
        {
            "temperature": 41,
            "pressure": 1.6
        },
        {
            "temperature": 24,
            "pressure": 1.9
        }
    ],
    "rain_front_name": "front rain tire",
    "rain_front_notes": "front rain tire",
    "rain_front_pressure": [
        {
            "temperature": 42,
            "pressure": 1.9
        },
        {
            "temperature": 22,
            "pressure": 1.5
        }
    ],
    "rain_rear_name": "rear rain tire",
    "rain_rear_notes": "rear rain tire",
    "rain_rear_pressure": [
        {
            "temperature": 45,
            "pressure": 1.5
        },
        {
            "temperature": 30,
            "pressure": 1.5
        }
    ],
    "setup": [
        {
            "category": "Motor",
            "group": None,
            "name": "Pwr Mode",
            "ticks_available": 2,
            "ticks_current": 2,
            "ticks_standard": 2
        },
        {
            "category": "Chassis",
            "group": "Shock",
            "name": "Rebound",
            "ticks_available": 29,
            "ticks_current": 12,
            "ticks_standard": 11
        }
    ]
}


def get(app, client):
    response = client.get("/api/bike", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def post(app, client, payload=None):
    if payload is None:
        payload = default_payload_post
    response = client.post("/api/bike", data=json.dumps(payload), content_type='application/json',
                           headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def get_item(app, client, id_):
    response = client.get(f"/api/bike/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def put_item(app, client, id_, payload=None):
    if payload is None:
        payload = default_payload_put
    response = client.put(f"/api/bike/{id_}", data=json.dumps(payload), content_type='application/json',
                          headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def delete_item(app, client, id_):
    response = client.delete(f"/api/bike/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response
