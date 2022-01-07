import os
import io
from backend.app import create_app
from backend.config import TestConfig


def test_route_assets():
    app = create_app(TestConfig)

    # test assets
    assets = [
        "coach-category-fork.svg",
        "coach-category-shock.svg"
    ]
    for asset in assets:
        # setup client
        client = app.test_client()
        url = "/assets/" + asset
        response = client.get(url)

        # get expected file
        dist_dir = app.config['DIST_DIR']
        entry = os.path.join(dist_dir, 'assets', asset)
        with open(entry, "rb") as file:
            asset_file = io.BytesIO(file.read())

        # test response vs expected
        assert response.get_data() == asset_file.read()
        assert response.status_code == 200

    # test access to files from other
    asset = "../favicon.svg"

    # setup client
    client = app.test_client()
    url = "/assets/" + asset
    response = None
    try:
        response = client.get(url)  # must throw an error!
    except (Exception,):
        pass

    # get expected file
    dist_dir = app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'assets', asset)
    with open(entry, "rb") as file:
        asset_file = io.BytesIO(file.read())

    # test response vs expected
    assert response is None
