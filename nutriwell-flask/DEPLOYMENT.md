# Deployment Checklist

The project can be deployed as a standard Python web service. The supplied `Procfile`, `wsgi.py`, `requirements.txt`, and `runtime.txt` provide the common configuration expected by Procfile-compatible hosts.

| Requirement | Included configuration |
| --- | --- |
| Python dependencies | `requirements.txt` |
| Production command | `Procfile` using Gunicorn |
| WSGI application | `wsgi.py` exporting `app` |
| Python runtime | `runtime.txt` |
| Static files and local images | `static/` directory |

Before deployment, set `SECRET_KEY` to a long random string in the host environment. Configure the hosting service to use the platform-provided `PORT`; the included production command already binds Gunicorn to that value.

> The contact form is intentionally presented as an on-screen confirmation workflow. Connect it to a mail provider or CRM before accepting production enquiries.

