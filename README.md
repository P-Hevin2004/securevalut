# SecureValut 🔐
A beautiful, responsive file sharing web app built with Django — upload, manage, and securely share files with ease.

[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Issues](https://img.shields.io/github/issues/Dhruv-4985/securevalut)](https://github.com/Dhruv-4985/securevalut/issues)

Live demo (optional): https://your-demo-url.example.com

Overview
--------
SecureValut is a simple, secure, and responsive Django-based file sharing system. It focuses on usability and mobile-first design so users can upload, manage, share, and download files from any device.

Why this README?
----------------
This new README highlights the app’s responsive UI, key features, setup steps, and visual assets so contributors and users can quickly evaluate, run, and test the project.

Key Features
------------
- Responsive, mobile-friendly UI (desktop/tablet/phone supported)
- User registration & authentication
- Upload files with title & description
- Public or private visibility per file
- Auto-generated shareable links for public files
- Protected access for private files (login / share-code)
- Download analytics (counts)
- Admin management via Django Admin

Quick screenshots
----------------
Add screenshots/gifs to the repo at /assets/ (e.g. assets/screenshot-desktop.png, assets/screenshot-mobile.png, assets/demo.gif)

Example:

- Desktop view: assets/screenshot-desktop.png
- Mobile view: assets/screenshot-mobile.png
- Live demo / responsive interaction: assets/demo.gif

Responsive UI notes
-------------------
The frontend uses a responsive layout so the app adapts across device widths. Suggested CSS stacks:
- Tailwind CSS or Bootstrap for utility-first responsive classes
- CSS Grid / Flexbox for file cards and dashboard
- Accessible color contrast and keyboard navigation for forms

Tech stack
----------
- Backend: Django
- Database: SQLite (dev) / PostgreSQL (recommended for prod)
- Frontend: HTML5, CSS3, responsive framework (Bootstrap/Tailwind), optional Vanilla JS
- Storage: local MEDIA (dev) / S3-compatible for production

Get started — development (quick)
-------------------------------
Clone, install, migrate, run:

```bash
git clone https://github.com/Dhruv-4985/securevalut.git
cd securevalut

python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt

# create .env or set env vars (see Configuration)
python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py runserver
```

Open: http://127.0.0.1:8000

Configuration
-------------
Create a .env (or set environment variables) with values similar to:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
MEDIA_ROOT=./media
MEDIA_URL=/media/
```

For production:
- Use a strong SECRET_KEY
- DEBUG=False
- Configure secure storage (S3) and a production-ready DB (Postgres)
- Configure HTTPS and ALLOWED_HOSTS

Deployment tips
---------------
- Serve static files via a CDN or nginx + WhiteNoise
- Use Gunicorn + nginx for best performance
- Configure environment variables via your host (Heroku, DigitalOcean App Platform, etc.)

Testing
-------
Run the Django test suite:

```bash
python manage.py test
```

Accessibility & UX
------------------
- Use semantic HTML and aria attributes for controls
- Ensure forms provide helpful validation messages
- Ensure keyboard accessibility for file cards and share modal

Contributing
------------
Contributions are welcome! Suggested workflow:
1. Fork the repo
2. Create a topic branch: git checkout -b feat/responsive-ui
3. Make changes, add/update tests and screenshots in /assets
4. Push and open a PR with a short description of changes

Please open issues for bugs or enhancement ideas.

Ideas for improving UI/UX
- Add drag-and-drop upload on desktop
- Add progress bar for large uploads (AJAX)
- Make share modal with optional expiration and password protection
- Add user profile page to manage uploaded files and settings

Project structure (high-level)
------------------------------
- securevalut/        - Django project settings
- app/                - main app: models, views, forms, templates, static
- templates/          - HTML templates (use responsive layouts)
- static/             - CSS, JS, images
- assets/             - screenshots, demo GIFs (add these)
- requirements.txt

FAQ / Troubleshooting
---------------------
- Media files not showing?
  - Check MEDIA_URL and MEDIA_ROOT in settings and that Django serves media in dev.
- Upload fails?
  - Check FILE_UPLOAD_MAX_MEMORY_SIZE and file permissions.
- Database errors?
  - Run python manage.py migrate

License
-------
MIT — see LICENSE

Contact
-------
Maintainer: Dhruv-4985
GitHub: https://github.com/Dhruv-4985/securevalut

What's next
-----------
- Add the visual assets (screenshots and demo GIF) to /assets in the repo so this README renders beautifully.
- If you want, I can commit this README.md for you on a new branch and open a PR; say "commit README" and I'll prepare the branch and push the file.
