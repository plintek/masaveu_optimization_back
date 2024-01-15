pip install -r /api/requirements.txt

if [ ! -d "/api/media" ]; then
    mkdir /api/media
fi

max_tries=10

while [ $max_tries -gt 0 ]; do
    echo "Waiting for postgres to be ready..."
    nc -z -v -w30 postgis 5432 && break
    max_tries=$((max_tries-1))
    sleep 2
done 

python3 /api/manage.py collectstatic --noinput --clear
python3 /api/manage.py makemigrations users --noinput

if [ -f /api/control.txt ]; then
    python3 /api/manage.py makemigrations 

else 
    touch /api/control.txt
    python3 /api/manage.py makemigrations users
fi
python3 /api/manage.py migrate users --noinput
python3 /api/manage.py migrate --noinput

python3 /api/manage.py migrate --run-syncdb --noinput
python3 /api/manage.py create_default_users

gunicorn -c /api/gunicorn/config/dev.py --preload --reload

tail -F /var/log/gunicorn/django.log