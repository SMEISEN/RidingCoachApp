import json
from datetime import datetime, timezone


def validate_filter_by(payload, post_query, app, client):
    response = post_query(app, client, payload)
    items = json.loads(response.get_data())
    assert isinstance(items, list)
    for item in items:
        for key, value in payload.items():
            assert item[key] == value
    assert response.status_code == 200


def validate_filter_intervals(payload, post_query, app, client):
    response = post_query(app, client, payload)
    items = json.loads(response.get_data())
    for item in items:
        for key in payload:
            if "datetime" in key:
                assert item[key] >= datetime.fromtimestamp(
                    payload[key]["values"][0], tz=timezone.utc).replace(tzinfo=None) \
                    .isoformat()  # this should be unified
                assert item[key] <= datetime.fromtimestamp(
                    payload[key]["values"][1], tz=timezone.utc).replace(tzinfo=None) \
                    .isoformat()  # this should be unified
            else:
                assert item[key] >= payload[key]["values"][0]
                assert item[key] <= payload[key]["values"][1]
    assert response.status_code == 200
