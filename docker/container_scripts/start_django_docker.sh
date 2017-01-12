#!/usr/bin/env bash
set -xe
chown -R rabbitmq:rabbitmq /data
rabbitmq-server -detached
sleep 30
rabbitmqctl add_user chuser chapss # add user for celery
rabbitmqctl set_permissions -p "/" chuser ".*" ".*" ".*" # give all permissions
python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('chuser', 'chuser@computationalhealthcare.com', 'super')" | python manage.py shell # superuser for django
python manage.py runserver 0.0.0.0:8000