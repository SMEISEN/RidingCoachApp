import json

default_payload_post = {
    "category": "name",
    "symptom": {
        "id": "example ID",
        "name": "example name"
    },
    "notes": "notes on the symptom",
    "questions": [
        "example question 1",
        "example question 2"
    ],
    "advice": {
        "A": {
            "problem": "problem A description",
            "solution": [
                "solution approach 1 of the problem",
                "solution approach 2 of the problem"
            ]
        },
        "B": {
            "problem": "problem B description",
            "solution": [
                "solution approach 1 of the problem",
                "solution approach 2 of the problem"
            ]
        }
    }
}

default_payload_put = {
    "category": "Name",
    "symptom": {
        "id": "ID example",
        "name": "name example"
    },
    "notes": "symptom notes",
    "questions": [
        "example question I",
        "example question II"
    ],
    "advice": {
        "a": {
            "problem": "problem a description",
            "solution": [
                "solution approach I of the problem",
                "solution approach II of the problem"
            ]
        },
        "b": {
            "problem": "problem b description",
            "solution": [
                "solution approach I of the problem",
                "solution approach II of the problem"
            ]
        }
    }
}


def get(app, client):
    response = client.get("/api/coach", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def post(app, client, payload=None):
    if payload is None:
        payload = default_payload_post
    response = client.post("/api/coach", data=json.dumps(payload), content_type='application/json',
                           headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def get_item(app, client, id_):
    response = client.get(f"/api/coach/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def put_item(app, client, id_, payload=None):
    if payload is None:
        payload = default_payload_put
    response = client.put(f"/api/coach/{id_}", data=json.dumps(payload), content_type='application/json',
                          headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def delete_item(app, client, id_):
    response = client.delete(f"/api/coach/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response
