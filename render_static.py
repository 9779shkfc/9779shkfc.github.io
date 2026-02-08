from app import app  # or create_app
from flask import url_for
import pathlib, os

app.testing = True
client = app.test_client()

routes = [
    '/', '/celebrity/kao', '/celebrity/jane'  # list all routes you want exported
]

out = pathlib.Path('public')
out.mkdir(exist_ok=True)

for route in routes:
    resp = client.get(route)
    if resp.status_code == 200:
        path = out / (route.strip('/').replace('/', '_') or 'index')
        if not path.suffix:
            path = path.with_suffix('.html')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(resp.data)

# copy static files
import shutil
if os.path.exists('static'):
    shutil.copytree('static', out / 'static', dirs_exist_ok=True)
