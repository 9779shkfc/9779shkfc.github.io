# Fan Club Site

A minimal, deployable Flask fan club site. This README is ready to paste into your repository at **`https://github.com/9779shkfc/fan-club-site` ** and includes exact commands for **Windows PowerShell** (your OS) and optional macOS/Linux commands.

---

## Repository
**GitHub:** `https://github.com/9779shkfc/fan-club-site` 

---

## Project overview
Small Flask site with:
- Homepage (Linktree + two images)
- Celebrity pages served by blueprints
- Static assets in `static/` (CSS, JS, fonts, images, music, favicon)
- Background music player (optional)
- Ready for deployment with Gunicorn

---

## Project structure
```
project-root/
├─ app.py
├─ requirements.txt
├─ Procfile
├─ .gitignore
├─ README.md
├─ blueprints/
│  ├─ kao.py
│  ├─ jane.py
│  └─ love_design.py
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ celebrity.html
│  └─ partials/
│     ├─ celebrity_header.html
│     └─ celebrity_content.html
└─ static/
   ├─ css/style.css
   ├─ js/site.js
   ├─ fonts/
   ├─ images/
   ├─ music/
   └─ favicon.ico
```

---

## Prerequisites
- **Python 3.11** (or 3.10+)
- **Git** installed and configured
- GitHub account (repo: `https://github.com/9779shkfc/fan-club-site`)
- Render account (optional) for deployment

---

## Setup (Windows PowerShell — exact commands for your OS)

1. **Open PowerShell** and go to project root:
```powershell
cd C:\path\to\project-root
```

2. **Create and activate virtual environment**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. **Upgrade pip and install dependencies**
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. **If you need to generate `requirements.txt`**
```powershell
pip freeze > requirements.txt
```

5. **Run the app (development)**
```powershell
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run
# Open http://127.0.0.1:5000
```

6. **Run with Gunicorn (use WSL on Windows for Gunicorn)**
- If you have WSL installed, open WSL and run:
```bash
# inside WSL (Ubuntu)
source .venv/bin/activate
gunicorn app:app --bind 0.0.0.0:8000
```
- Or deploy to a host (Render) which runs Gunicorn on Linux.

---

## Setup (macOS / Linux — optional)
```bash
cd /path/to/project-root
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
# or
gunicorn app:app --bind 127.0.0.1:8000
```

---

## Git and GitHub (push steps)

1. **Initialize and commit (PowerShell)**
```powershell
cd C:\path\to\project-root
git init
git add .
git commit -m "Initial commit: Flask fan club site"
git branch -M main
```

2. **Add remote and push**
```powershell
git remote add origin https://github.com/9779shkfc/fan-club-site.git
git push -u origin main
```

If the remote already has commits:
```powershell
git pull --rebase origin main
git push
```

---

## Prepare for deployment

1. **Expose `app` in `app.py`**
```python
app = create_app()
if __name__ == '__main__':
    app.run()
```

2. **Procfile** (repo root)
```
web: gunicorn app:app
```

3. **requirements.txt** must include:
```
Flask
gunicorn
# plus any other libraries you use
```

4. **.gitignore** should exclude:
```
.venv/
__pycache__/
*.pyc
.env
instance/
.DS_Store
.vscode/
.idea/
*.log
```

5. **Environment variables** (do not commit secrets)
- `SECRET_KEY` (set on host)

---

## Deploy to Render (recommended)

1. Sign in to Render and connect GitHub.
2. Click **New → Web Service** and select `9779shkfc/fan-club-site`.
3. Branch: `main`.
4. Build command: leave blank (Render runs `pip install -r requirements.txt`) or set:
```
pip install -r requirements.txt
```
5. Start command:
```
gunicorn app:app
```
6. Add environment variables in Render dashboard:
- `SECRET_KEY` = *your secure value*
7. Create Web Service and wait for build/deploy. Open the provided URL.

---

## Common troubleshooting

- **git not recognized**: install Git for Windows and restart PowerShell.
- **Static files 404**: use `{{ url_for('static', filename='path') }}` and confirm files are committed.
- **Favicon 404**: ensure `static/favicon.ico` exists and `base.html` links to it.
- **Fonts cached**: clear browser cache or test in incognito.
- **Large audio files**: avoid committing large files to GitHub; use external storage or Git LFS.
- **Deployment errors**: check Render build logs; common fixes are missing dependencies in `requirements.txt` or wrong Gunicorn entrypoint.

---

## Useful commands summary (Windows PowerShell)
```powershell
# Activate venv
.venv\Scripts\Activate.ps1

# Install deps
pip install -r requirements.txt

# Generate requirements
pip freeze > requirements.txt

# Run dev server
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run

# Git
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/9779shkfc/fan-club-site.git
git push -u origin main
```

---

## Notes
- Replace `SECRET_KEY` with a secure random value on your host.
- If you later want automatic playlist generation from `static/music/`, I can provide a small server-side script to generate `<source>` tags dynamically.
- If your GitHub username differs from `9779shkfc`, update the repository URL in the Git commands accordingly.

---

**Done.** Paste this `README.md` into the root of your repo and commit. If you want, I can also create a short `LICENSE` file or a `.github/workflows` CI workflow for automated tests and deploys.
