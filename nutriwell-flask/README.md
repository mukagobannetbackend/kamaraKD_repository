# NutriWell Flask Website

This folder is a **deployment-ready Flask website** created with Flask, HTML, CSS, and vanilla JavaScript. It includes responsive layouts, completed informational pages for every navigation link, locally stored image assets, and a light/dark theme switcher.

## Run locally

```bash
cd flask_app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Open `http://127.0.0.1:5000` in your browser.

## Production deployment

Set a strong `SECRET_KEY` environment variable and install dependencies from `requirements.txt`. The included `Procfile` starts the project with Gunicorn on platforms that support Procfiles:

```bash
gunicorn --workers 3 --bind 0.0.0.0:$PORT wsgi:app
```

The `static/images/` directory must remain included when deploying. The contact form currently confirms submissions on-screen; connect it to your preferred email or CRM before collecting real enquiries.

| Location | Purpose |
| --- | --- |
| `app.py` | Flask routes and page-content data |
| `templates/` | Reusable base layout and page templates |
| `static/css/style.css` | Responsive visual system and dark mode |
| `static/js/main.js` | Theme toggle, mobile navigation, and motion |
| `static/images/` | Local website imagery and logo asset |
