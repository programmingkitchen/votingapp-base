# Vote App

# Description
This is a Dockerfied app that uses a login system but does not use a registration
sysem or Flask Blueprints.

It is designed to be an ideal format for simple apps (not so big where
blueprints are essential) and security is controlled by only allowing users who
where manually

## HELPFUL INFO
### Set alias for Local Microservice/Web App
alias vrun='cd  ~/Dropbox/PYTHON-PROGRAMS/FLASK/VOTE-SIMPLE-TEMPLATE-1/vote; pwd; python wsgi.py'
alias vsrc='cd ~/Dropbox/PYTHON-PROGRAMS/FLASK/VOTE-SIMPLE-TEMPLATE-1/vote; pwd'

### REPO NAMES
https://github.com/programmingkitchen/votingapp-base.git
https://hub.docker.com/repository/docker/rgranier/<NEW_NAME>


## REQUIREMENTS

NOTE:  These are currently installed, but not all may be necessary

It uses:
WTforms
SQLalchemy
sqlite

## TO DO
1. Implement safe_url
https://flask-login.readthedocs.io/en/latest/
if not is_safe_url(next):
            return flask.abort(400)

2. Registration System option.

3. Admin login

4. Reset DB as Admin.
