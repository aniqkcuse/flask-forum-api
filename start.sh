#!/bin/sh

if [ "$DATABASE" = "mysql" ]
then
  echo "Waiting for mysql..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "Mysql started"
fi

flask --app run db init
flask --app run db migrate -m "Initial migration"
flask --app run db upgrade

exec "$@"
