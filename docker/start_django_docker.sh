#!/usr/bin/env bash
set -xe
chown -R rabbitmq:rabbitmq /data
rabbitmq-server -detached
sleep 30
rabbitmqctl add_user chuser chapss
rabbitmqctl set_permissions -p "/" chuser ".*" ".*" ".*"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('chuser', 'chuser@computationalhealthcare.com', 'super')" | python manage.py shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000