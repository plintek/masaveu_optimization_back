#! /bin/bash

#------
pip install -r /back/api/requirements.txt
rm -fr /back/api/users/migrations/*

# python3 /back/api/manage.py collectstatic --noinput

python3 /back/api/manage.py makemigrations 

python3 /back/api/manage.py migrate 

# python3 /back/api/manage.py makemessages

python3 /back/api/manage.py compilemessages


# python3 /back/api/manage.py loaddata data/*   # Remove line if not data at startup

python3 /back/api/manage.py create_default_users




python3 /back/api/manage.py runserver 0.0.0.0:8000
