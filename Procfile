release: python manage.py migrate
web: gunicorn characters.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate
