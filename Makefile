all: setup_py setup_coveralls setup_js setup_django

ci: setup_ci all

staging: create-staging update-staging

define resetdb_to_backup
	dropdb $1
	createdb $1
	pg_restore -O -x -n public -d $1 ~hacklab/sql-backup/last.psqlc
endef

define reset_media
	rm -rf ~/webfiles/media/
	cp -r ~timtec-production/webfiles/media ~/webfiles/
endef

define base_update
	cp timtec/settings_local_$1.py timtec/settings_local.py
	~/env/bin/pip install --upgrade pip
	~/env/bin/pip install -U -r requirements/test.txt
	npm install
	~/env/bin/python manage.py migrate --noinput --fake-initial
	~/env/bin/python manage.py collectstatic --noinput
	~/env/bin/python manage.py compilemessages
	touch ~/wsgi-reload
endef

update:
	~/env/bin/pip install --upgrade pip
	~/env/bin/pip install -U -r requirements/production.txt
	npm install
	~/env/bin/python manage.py migrate --noinput --fake-initial
	~/env/bin/python manage.py collectstatic --noinput
	~/env/bin/python manage.py compilemessages
	touch ~/wsgi-reload

install:
	virtualenv ~/env
	~/env/bin/pip install --upgrade pip
	~/env/bin/pip install -r requirements/production.txt
	npm install
	mkdir -p ~/webfiles/static
	mkdir -p ~/webfiles/media
	cp timtec/settings_local.py.template timtec/settings_local.py
	~/env/bin/python manage.py migrate --noinput
	~/env/bin/python manage.py loaddata initial
	~/env/bin/python manage.py collectstatic --noinput
	~/env/bin/python manage.py compilemessages
	touch ~/wsgi-reload

create-staging:
	virtualenv ~/env
	~/env/bin/pip install -r requirements/production.txt
	npm install
	mkdir -p ~/webfiles/static
	mkdir -p ~/webfiles/media

create-production: create-staging
	cp timtec/settings_local_production.py timtec/settings_local.py
	cp ../settings_production.py timtec/settings_production.py
	~/env/bin/python manage.py syncdb --noinput --no-initial-data
	~/env/bin/python manage.py migrate --noinput --no-initial-data
	~/env/bin/python manage.py collectstatic --noinput
	~/env/bin/python manage.py compilemessages
	touch ~/wsgi-reload

update-test:
	$(call resetdb_to_backup,timtec-test)
	$(call reset_media)
	$(call base_update,test)

update-dev:
	$(call resetdb_to_backup,timtec-dev)
	$(call reset_media)
	$(call base_update,timtec_dev)

update-demo:
	$(call base_update,demo)

update-staging:
	$(call base_update,staging)

update-ifsul:
	$(call base_update,ifsul)

update-design:
	$(call base_update,design)

update-production:
	cp ../settings_production.py timtec/settings_production.py
	$(call base_update,production)

test_collectstatic: clean
	py.test --collectstatic tests/test_collectstatic.py

clean:
	find . -type f -name '*.py[co]' -exec rm {} \;

python_tests: clean
	py.test --pep8 --flakes --splinter-webdriver=phantomjs --cov . . $*

js_tests:
	find . -path ./bower_components -prune -o -path bower_components/ -prune -o -path ./node_modules -prune -o -regex ".*/vendor/.*" -prune -o -name '*.js' -exec ./node_modules/jshint/bin/jshint {} \;

all_tests: clean python_tests js_tests test_collectstatic

setup_ci:
	psql -c 'create database timtec_ci;' -U postgres
	pip install --upgrade pip
	cp timtec/settings_local_ci.py timtec/settings_local.py

setup_py:
	pip install -r requirements/test.txt
	python setup.py -q develop

setup_coveralls:
	pip install -q coveralls

setup_js:

	npm install # --loglevel silent

setup_django: clean
	python manage.py migrate --noinput
	python manage.py loaddata initial
	python manage.py compilemessages

dumpdata: clean
	@python manage.py dumpdata --indent=2 -n -e south.migrationhistory -e admin.logentry -e socialaccount.socialaccount -e socialaccount.socialapp -e sessions.session -e contenttypes.contenttype -e auth.permission -e account.emailconfirmation -e socialaccount.socialtoken

dumpcourses:
	python manage.py dumpdata --indent=2 -n -e south -e admin -e socialaccount -e sessions -e contenttypes -e auth -e account -e accounts -e notes| gzip -9 > courses.json.gz

reset_db: clean
	python manage.py reset_db --router=default --noinput -U $(USER)
	python manage.py syncdb --noinput
	python manage.py migrate --noinput

messages: clean
	python manage.py makemessages -a -d django

docker_dev:
	docker-compose -f docker-compose-dev.yml up

docker_dev_build:
	docker-compose -f docker-compose-dev.yml build

doc_install:
	virtualenv docs/env
	make doc_update

doc_update:
	docs/env/bin/pip install --upgrade pip
	docs/env/bin/pip install -U -r docs/requirements.txt

doc_build:
	make doc_update
	docs/env/bin/mkdocs build

doc_run:
	make doc_update
	docs/env/bin/mkdocs serve

docker_dev:
