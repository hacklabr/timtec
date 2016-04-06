#!/usr/bin/env python

import os
import sys
import subprocess
import time
import django
import environ
import psycopg2

from django.conf import settings
from django.core.management import execute_from_command_line

sys.path.insert(1, '/app/timtec')
env = environ.Env()
environ.Env.read_env('/app/.env')

command = ['supervisord', '-c', '/app/timtec/docker/supervisord.conf']
database = settings.DATABASES.get('default')

if sys.argv[1:] != command:
    subprocess.call(sys.argv[1:])
    sys.exit(0)

tries = 5
timeout = 5
exception = None

#
# Waiting for postgis start on docker-compose
#
while tries > 0:
    try:
        conn = psycopg2.connect(
            user='postgres',
            host='postgres',
            password=env('POSTGRES_ENV_POSTGRES_PASSWORD')
        )
        tries = 0
        exception = None
    except psycopg2.OperationalError as e:
        exception = e
        tries = tries - 1
        sys.stderr.write('Failed to connect to postgres, %d tries reamaining...\n' % tries)
        time.sleep(timeout)

if exception:
    raise exception

conn.set_isolation_level(0)
cur = conn.cursor()

cur.execute("SELECT count(1) > 0 FROM pg_user WHERE usename='%(USER)s';" % database)
user_exists = cur.fetchone()[0]

cur.execute("SELECT count(1) FROM pg_database WHERE datname='%(NAME)s';" % database)
db_exists = cur.fetchone()[0]

if not user_exists:
    cur.execute("CREATE USER %(USER)s WITH PASSWORD '%(PASSWORD)s';" % database)

if not db_exists:
    cur.execute("CREATE DATABASE %(NAME)s OWNER %(USER)s;" % database)
    cur.close()
    conn.close()

    conn = psycopg2.connect(
        dbname=database.get('NAME'),
        user='postgres',
        host='postgis',
        password=env('POSTGRES_ENV_POSTGRES_PASSWORD')
    )
    conn.set_isolation_level(0)
    cur = conn.cursor()

cur.close()
conn.close()

execute_from_command_line(['manage.py', 'migrate'])
execute_from_command_line(['manage.py', 'loaddata', 'initial'])

subprocess.call(sys.argv[1:])
