import json

default_payload_post = {
    "name": "spare part name",
    "module": "Engine",
    "min_stock": 2
}

default_payload_put = {
    "name": "name spare part",
    "module": "Suspension",
    "min_stock": 1
}

default_payload_query = {
    "name": "spare part name",
    "module": "Engine",
    "min_stock": {
        "values": [
            0,
            2
        ],
        "operators": [
            ">=",
            "<="
        ]
    }
}


def get(app, client):
    response = client.get("/api/sparepart", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def post(app, client, payload=None):
    if payload is None:
        payload = default_payload_post

    response = client.post("/api/sparepart", data=json.dumps(payload), content_type='application/json',
                           headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def get_item(app, client, id_):
    response = client.get(f"/api/sparepart/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def put_item(app, client, id_, payload=None):
    if payload is None:
        payload = default_payload_put
    response = client.put(f"/api/sparepart/{id_}", data=json.dumps(payload), content_type='application/json',
                          headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def delete_item(app, client, id_):
    response = client.delete(f"/api/sparepart/{id_}", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def post_query(app, client, payload=None):
    if payload is None:
        payload = default_payload_query

    response = client.post("/api/sparepart/query", data=json.dumps(payload), content_type='application/json',
                           headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response


def get_warnings(app, client):
    response = client.get("/api/sparepart/warnings", headers={"apikey": app.config['FLASK_RESTPLUS_API_KEY']})

    return response
