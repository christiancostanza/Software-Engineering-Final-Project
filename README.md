# Software-Engineering-Final-Project

> Short description: A Flask-based web app (group final project). This repo contains the web application, static assets, templates, and utilities required to run the app locally and deploy to a platform such as Azure App Service or Heroku.
> Worked in a four person group and developed a web app to allow you to create your own personal cookbook. Pulling from an api for recipes it allows you to save those recipes and search for new recipes based on various tags, such as dietary restrictions or finding recipes based on what you have on hand.
> I personally contributed to much of the front end as well as the connection of front and backend as well as assisting with the implementation of the database.

## Features
- Flask backend (`app.py`)
- Azure SQL connector utility (`azuresqlconnector.py`)
- Jinja2 templates in `templates/`
- Static assets in `static/` (CSS, JS)

## Requirements
- Python 3.8+ (use virtualenv)
- `pip` to install dependencies listed in `requirements.txt`

## Setup (local)
```bash
# 1. unzip or place project files into a folder
# 2. create a clean git repo (or follow prepare_repo.sh)
python -m venv venv
source venv/bin/activate    # macOS / Linux
venv\Scripts\activate     # Windows (PowerShell)

pip install -r requirements.txt

# create .env with configuration variables, e.g.:
# FLASK_ENV=development
# FLASK_APP=app.py
# AZURE_SQL_CONN_STRING="<your connection string>"

export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Navigate to `http://127.0.0.1:5000` to view the app.


## Deployment notes
### Azure App Service
- Ensure `requirements.txt` and `startup` (or `gunicorn`) command provided in App Service settings.
- Store secrets (DB connection string) in App Service configuration rather than in code.


## Remove embedded `.git` folder
The uploaded zip includes a `.git` folder from the original project. To create a clean repository, remove or rename the `.git` folder before initializing a new remote repo. Use the provided `prepare_repo.sh` helper.
