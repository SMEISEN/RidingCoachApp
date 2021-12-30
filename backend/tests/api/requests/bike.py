import json

default_payload = {
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


def post(app, client, payload=None):
    if payload is None:
        payload = default_payload
    response = client.post("/api/bike", data=json.dumps(payload), content_type='application/json',
                           headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response
