import os
import io
from backend.app import app


def test_route_index():
    # setup client
    client = app.test_client()
    url = "/"
    response = client.get(url)

    # get expected file
    dist_dir = app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    with open(entry, "rb") as file:
        index_html = io.BytesIO(file.read())

    # test response vs expected
    assert response.get_data() == index_html.read()
    assert response.status_code == 200
