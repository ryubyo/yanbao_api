# Startup
DEV:
nohup python manage.py runserver localhost:6777 >> ./nohup.out 2>&1 &

PROD:
nohup python manage.py runserver 0.0.0.0:6777 >> ./nohup.out 2>&1 &