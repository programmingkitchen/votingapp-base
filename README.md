# Vote App

# Description
This app uses a login system but does not use Flask Blueprint.
It is designed to be an ideal format for simple apps (not so big where
blueprints are essential).

It uses:
WTforms
SQLalchemy
sqlite

## HOW TO RUN APP LOCALLY

# Set alias for Local Microservice/Web App
alias vrun='cd  ~/Dropbox/PYTHON-PROGRAMS/FLASK/VOTE-SIMPLE-TEMPLATE-1/vote; pwd; python wsgi.py'
alias vsrc='cd ~/Dropbox/PYTHON-PROGRAMS/FLASK/VOTE-SIMPLE-TEMPLATE-1/vote; pwd'


## REQUIREMENTS

NOTE:  These are currently installed, but not all may be necessary

alembic==1.6.5
aniso8601==9.0.1
click==8.0.1
colorama==0.4.4
Flask==2.0.1
Flask-HTTPAuth==4.4.0
Flask-Login==0.5.0
Flask-Migrate==3.1.0
Flask-RESTful==0.3.9
Flask-SQLAlchemy==2.5.1
Flask-WTF==0.15.1
greenlet==1.1.1
importlib-metadata==4.6.3
itsdangerous==2.0.1
Jinja2==3.0.1
Mako==1.1.4
MarkupSafe==2.0.1
python-dateutil==2.8.2
python-editor==1.0.4
pytz==2021.1
six==1.16.0
SQLAlchemy==1.4.22
typing-extensions==3.10.0.0
Werkzeug==2.0.1
WTForms==2.3.3
zipp==3.5.0

## TO DO
Implement safe_url
https://flask-login.readthedocs.io/en/latest/
if not is_safe_url(next):
            return flask.abort(400)
