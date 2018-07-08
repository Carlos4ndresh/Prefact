#!/bin/bash
sleep 20;

# git clone https://github.com/Carlos4ndresh/Prefact.git /srv/Prefact/Prefact
git clone --single-branch -b AutoGeneradoProyectos https://github.com/Carlos4ndresh/Prefact.git /srv/Prefact/Prefact

pip install -r /srv/Prefact/Prefact/requirements.txt


python manage.py migrate                  # Apply database migrations

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='carlos.herrera@outlook.com', is_superuser=True).delete(); User.objects.create_superuser('cherrera', 'carlos.herrera@outlook.com', 'nimda')" | python manage.py shell


python manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn prefact.wsgi:application \
    --name Defina \
    --bind 0.0.0.0:8008 \
    --workers 3 \
    --log-level=info \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log \
    "$@"