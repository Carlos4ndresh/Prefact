#!/bin/bash
# while ! nc -z mysqldb 33066; 
#     do 
#         echo sleeping; 
#         sleep 1; 
#     done; 
#     python manage.py migrate                  # Apply database migrations
#     python manage.py collectstatic --noinput  # Collect static files

#     # Prepare log files and start outputting logs to stdout
#     touch /srv/logs/gunicorn.log
#     touch /srv/logs/access.log
#     tail -n 0 -f /srv/logs/*.log &

#     # Start Gunicorn processes
#     echo Starting Gunicorn.
#     exec gunicorn prefact.wsgi:application \
#         --name Defina \
#         --bind 0.0.0.0:8000 \
#         --workers 3 \
#         --log-level=info \
#         --log-file=/srv/logs/gunicorn.log \
#         --access-logfile=/srv/logs/access.log \
#         "$@"
#     echo Connected!;

# sleep 30;

python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn prefact.wsgi:application \
    --name Defina \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log \
    "$@"