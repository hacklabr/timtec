FROM debian:jessie
MAINTAINER Fabio Montefuscolo <fabio.montefuscolo@hacklab.com.br>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install -y python python-pip python-dev \
    && apt-get install -y libpq-dev libjpeg-dev libpng12-dev gettext \
    && apt-get install -y nginx supervisor \
    && apt-get install -y npm git

RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install -g phantomjs-prebuilt bower

RUN useradd -m -d /app -u 1000 -s /bin/bash timtec
RUN mkdir -p /app

# Prefer to use mdillon/postgis
ENV DJANGO_DATABASE_URL='postgres://timtec:timtec@postgres/timtec'
ENV DJANGO_SETTINGS_MODULE='timtec.settings_local_docker'
ENV PYTHONPATH='/app/timtec'
ENV GUNICORN_LOG_LEVEL='info'
ENV GUNICORN_EXTRA_FLAGS=''

COPY . /app/timtec
RUN mkdir -p /app/webfiles/static \
   && mkdir -p /app/webfiles/media \
   && pip install -r /app/timtec/requirements/production.txt \
   && chown -R timtec /app

WORKDIR /app/timtec
USER timtec

RUN npm install \
   && node bower install \
   && node node_modules/grunt-cli/bin/grunt \
   && python manage.py compilemessages \
   && python manage.py collectstatic --noinput \
   && python manage.py compile_pyc --path /app/timtec \
   && python manage.py collectstatic --noinput

USER root
EXPOSE 80 8000

CMD ["supervisord", "-c", "/app/timtec/docker/supervisord.conf"]
