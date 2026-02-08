# render_static.py
# Robust static exporter that prefers create_app(), sets SERVER_NAME so url_for works,
# auto-discovers simple GET routes, tries common home paths, and falls back to README.md.
import importlib
import traceback
import shutil
import os
from pathlib import Path

print("render_static.py starting")
print("cwd:", os.getcwd())
import sys
print("python:", sys.version.splitlines()[0])

# --- import app (prefer factory create_app if present) ---
app = None
try:
    mod = importlib.import_module('app')  # change 'app' if your module name differs
    if hasattr(mod, 'create_app'):
        app = mod.create_app()
        print("Used create_app() from module 'app'")
    else:
        app = getattr(mod, 'app')
        print("Used top-level 'app' from module 'app'")
except Exception:
    print("Importing 'app' failed, trying other common module names")
    traceback.print_exc()
    # try a few other common module paths
    candidates = ['fanclub', 'src.app', 'create_app']
    for c in candidates:
        try:
            mod = importlib.import_module(c)
            if hasattr(mod, 'create_app'):
                app = mod.create_app()
                print(f"Used create_app() from module '{c}'")
                break
            else:
                app = getattr(mod, 'app')
                print(f"Used top-level 'app' from module '{c}'")
                break
        except Exception:
            print(f"Import attempt failed for {c}")
            traceback.print_exc()

if app is None:
    print("Failed to import Flask app. Edit this script to match your project module name.")
    sys.exit(2)

# --- ensure url_for works outside a request context ---
if not app.config.get('SERVER_NAME'):
    app.config['SERVER_NAME'] = 'localhost'
app.config.setdefault('PREFERRED_URL_SCHEME', 'http')
print("App config SERVER_NAME:", app.config.get('SERVER_NAME'))
print("App config PREFERRED_URL_SCHEME:", app.config.get('PREFERRED_URL_SCHEME'))

# --- show available routes for debugging ---
try:
    print("App url_map rules:")
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: str(r)):
        print(f"  {rule}  methods={sorted(rule.methods)}  args={list(rule.arguments)}")
except Exception:
    print("Could not list url_map")
    traceback.print_exc()

app.testing = True
client = app.test_client()

# --- build list of candidate routes to try ---
home_candidates = ['/', '/index', '/index.html', '/home', '/main']
discovered = []
try:
    for rule in app.url_map.iter_rules():
        if 'GET' in rule.methods and len(rule.arguments) == 0:
            discovered.append(str(rule.rule))
    discovered = sorted(set(discovered), key=lambda p: (p != '/', p))
    if discovered:
        print("Auto-discovered routes:", discovered)
except Exception:
    print("Could not auto-discover routes")
    traceback.print_exc()

# Merge candidates: root first, then discovered, then common homes
candidates = []
for p in (['/'] + discovered + home_candidates):
    if p not in candidates:
        candidates.append(p)
print("Final route candidates to try:", candidates)

# --- export to public/ ---
out = Path('public')
if out.exists():
    print("Removing existing public/")
    shutil.rmtree(out)
out.mkdir(parents=True, exist_ok=True)

wrote_index = False

for route in candidates:
    try:
        print("Requesting route:", route)
        resp = client.get(route)
        print("Status:", resp.status_code, "Length:", len(resp.data))
        if resp.status_code == 200:
            if route == '/':
                target = out / 'index.html'
                wrote_index = True
            else:
                name = route.strip('/').replace('/', '_') or 'index'
                target = out / f'{name}.html'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(resp.data)
            print(f"Wrote {target}")
            if target.name == 'index.html':
                break
        else:
            print(f"Skipping {route}: status {resp.status_code}")
    except Exception:
        print("Error requesting route", route)
        traceback.print_exc()

# --- fallback: render index.html template directly ---
if not wrote_index:
    try:
        print("Fallback: rendering Jinja template 'index.html' if present")
        tmpl = app.jinja_env.get_template('index.html')
        html = tmpl.render()
        (out / 'index.html').write_text(html, encoding='utf-8')
        wrote_index = True
        print("Wrote public/index.html from template")
    except Exception:
        print("Template render fallback failed")
        traceback.print_exc()

# --- final fallback: convert README.md to index.html ---
if not wrote_index:
    try:
        print("Fallback: converting README.md to index.html")
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
            wrote_index = True
            print("Wrote public/index.html from README.md")
        else:
            print("No README.md found for fallback")
    except Exception:
        print("README fallback failed")
        traceback.print_exc()

# --- copy static assets ---
if Path('static').exists():
    try:
        shutil.copytree('static', out / 'static', dirs_exist_ok=True)
        print("Copied static/ to public/static")
    except Exception:
        print("Failed to copy static/")
        traceback.print_exc()
else:
    print("No static/ folder found")

print("Done. public/ contents:")
for p in sorted(out.rglob('*')):
    print(p.relative_to(out))


