#!/bin/bash
/app/wait-for-it.sh mysql:3306
export FLASK_APP=app.py
export EXE_ENV=container
flask db init
flask db migrate
flask db upgrade
uwsgi --ini /app/uwsgi.ini
