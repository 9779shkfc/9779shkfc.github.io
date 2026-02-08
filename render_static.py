# render_static.py
# Static exporter for Flask app with folder-based index.html

import importlib
import traceback
import shutil
import os
from pathlib import Path
import sys

print("render_static.py starting")
print("cwd:", os.getcwd())
print("python:", sys.version.splitlines()[0])

# --- import app (prefer factory create_app if present) ---
app = None
try:
    mod = importlib.import_module('app')  # adjust if your module name differs
    if hasattr(mod, 'create_app'):
        app = mod.create_app()
        print("Used create_app() from module 'app'")
    else:
        app = getattr(mod, 'app')
        print("Used top-level 'app' from module 'app'")
except Exception:
    print("Importing 'app' failed")
    traceback.print_exc()
    sys.exit(2)

# --- ensure url_for works outside a request context ---
if not app.config.get('SERVER_NAME'):
    app.config['SERVER_NAME'] = 'localhost'
app.config.setdefault('PREFERRED_URL_SCHEME', 'http')

app.testing = True
client = app.test_client()

# --- explicit routes to export ---
routes = [
    '/',                # homepage
    '/kao/',            # Kao page
    '/jane/',           # Jane page
    '/love-design/',    # Love Design page
    '/media/laptop/',   # Media laptop page
    '/media/mobile/'    # Media mobile page
]

# --- export to public/ ---
out = Path('public')
if out.exists():
    print("Removing existing public/")
    shutil.rmtree(out)
out.mkdir(parents=True, exist_ok=True)

for route in routes:
    try:
        print("Requesting route:", route)
        resp = client.get(route)
        print("Status:", resp.status_code, "Length:", len(resp.data))
        if resp.status_code == 200:
            if route == '/':
                target = out / 'index.html'
            else:
                folder = out / route.strip('/')
                target = folder / 'index.html'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(resp.data)
            print(f"Wrote {target}")
        else:
            print(f"Skipping {route}: status {resp.status_code}")
    except Exception:
        print("Error requesting route", route)
        traceback.print_exc()

# --- fallback: convert README.md to index.html if homepage missing ---
if not (out / 'index.html').exists():
    try:
        import markdown
        readme = Path('README.md')
        if readme.exists():
            md = readme.read_text(encoding='utf-8')
            body = markdown.markdown(md, extensions=['fenced_code', 'tables'])
            html = (
                "<!doctype html><html><head><meta charset='utf-8'>"
                "<meta name='viewport' content='width=device-width,initial-scale=1'>"
                "<title>Site</title></head><body>"
                f"{body}</body></html>"
            )
            (out / 'index.html').write_text(html, encoding='utf-8')
            print("Wrote public/index.html from README.md")
    except Exception:
        traceback.print_exc()

# --- copy static assets ---
if Path('static').exists():
    shutil.copytree('static', out / 'static', dirs_exist_ok=True)
    print("Copied static/ to public/static")

print("Done. public/ contents:")
for p in sorted(out.rglob('*')):
    print(p.relative_to(out))


