all: setup_py setup_coveralls setup_js setup_django

ci: setup_ci settings_ci all

create-staging:
	virtualenv ~/env
	~/env/bin/pip install -r requirements.txt
	mkdir -p ~/webfiles/static
	mkdir -p ~/webfiles/media

update-staging:
	cp timtec/settings_local_staging.py timtec/settings_local.py
	~/env/bin/pip install -r requirements.txt
	~/env/bin/python manage.py syncdb --all --noinput
	~/env/bin/python manage.py collectstatic --noinput
	~/env/bin/python manage.py compilemessages
	touch timtec/wsgi.py

staging: create-staging update-staging

create-production:
	virtualenv ~/env
	~/env/bin/pip install -r requirements.txt
	mkdir -p ~/webfiles/static
	mkdir -p ~/webfiles/media
	cp timtec/settings_local_production.py timtec/settings_local.py
	cp ../settings_production.py timtec/settings_production.py
	~/env/bin/pip install -r requirements.txt
	~/env/bin/python manage.py syncdb --noinput --no-initial-data
	~/env/bin/python manage.py migrate --noinput --no-initial-data
	~/env/bin/python manage.py loaddata production
	~/env/bin/python manage.py collectstatic --noinput
	~/env/bin/python manage.py compilemessages
	touch timtec/wsgi.py

update-production:
	cp timtec/settings_local_production.py timtec/settings_local.py
	~/env/bin/pip install -r requirements.txt
	~/env/bin/python manage.py syncdb --noinput
	~/env/bin/python manage.py migrate --noinput
	~/env/bin/python manage.py collectstatic --noinput
	~/env/bin/python manage.py compilemessages
	touch timtec/wsgi.py

test_collectstatic:
	python manage.py collectstatic --noinput -n

python_tests:
	find . -type f -name '*.py[co]' -exec rm {} \;
	py.test --pep8 --flakes --cov . . $*

karma_tests:
	karma start tests/confkarma.js $*

all_tests: test_collectstatic python_tests karma_tests

setup_ci:
	psql -c 'create database timtec_ci;' -U postgres

setup_py:
	pip install -q -r requirements.txt --use-mirrors
	pip install -q -r dev-requirements.txt --use-mirrors
	python setup.py -q develop

setup_coveralls:
	pip install -q coveralls --use-mirrors

setup_js:
	sudo `which npm` -g install less yuglify karma --loglevel silent

setup_django:
	python manage.py syncdb --all --noinput
	python manage.py compilemessages

settings_ci:
	cp timtec/settings_local_ci.py timtec/settings_local.py

dumpdata:
	python manage.py dumpdata --indent=2 -n -e south.migrationhistory -e admin.logentry -e socialaccount.socialaccount -e socialaccount.socialapp -e sessions.session -e contenttypes.contenttype -e auth.permission -e account.emailconfirmation -e socialaccount.socialtoken

reset_db:
	python manage.py reset_db --router=default --noinput -U $(USER)
	python manage.py syncdb --noinput
	python manage.py migrate --noinput
	python manage.py loaddata staging
