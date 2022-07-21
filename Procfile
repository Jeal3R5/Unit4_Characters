release: python manage.py migrate --no-input
web: gunicorn characters.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate
