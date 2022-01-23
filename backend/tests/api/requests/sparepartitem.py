import json
from backend.tests.api.requests.sparepart import post as post_sparepart

default_payload_post = {
    "condition": "good",
    "description": "new",
    "stock": 1,
}

default_payload_put = {
    "condition": "bad",
    "description": "used",
    "stock": 2,
}


def get(app, client):
    response = client.get("/api/sparepartitem", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def post(app, client, payload=None):
    if payload is None:
        payload = default_payload_post


    # post a spare part item first
    response = post_sparepart(app, client)
    payload["sparepart_id"] = json.loads(response.get_data())

    response = client.post("/api/sparepartitem", data=json.dumps(payload), content_type='application/json',
                           headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})
    payload.pop("sparepart_id")

    return response


def get_item(app, client, id_):
    response = client.get(f"/api/sparepartitem/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def put_item(app, client, id_, payload=None):
    if payload is None:
        payload = default_payload_put
    response = client.put(f"/api/sparepartitem/{id_}", data=json.dumps(payload), content_type='application/json',
                          headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def delete_item(app, client, id_):
    response = client.delete(f"/api/sparepartitem/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response
