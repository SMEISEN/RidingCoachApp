import os
import io
from backend.app import create_app
from backend.config import TestConfig


def test_route_favicon():
    app = create_app(TestConfig)

    # setup client
    client = app.test_client()
    url = "/favicon.svg"
    response = client.get(url)

    # get expected file
    dist_dir = app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'favicon.svg')
    with open(entry, "rb") as file:
        favicon_svg = io.BytesIO(file.read())

    # test response vs expected
    assert response.get_data() == favicon_svg.read()
    assert response.status_code == 200
