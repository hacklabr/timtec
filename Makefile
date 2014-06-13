all: setup_py setup_coveralls setup_js setup_django

ci: setup_ci settings_ci all

create-staging:
	virtualenv ~/env
	~/env/bin/pip install -r requirements.txt
	mkdir -p ~/webfiles/static
	mkdir -p ~/webfiles/media

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
	~/env/bin/python manage.py create_student_and_professor
	touch ~/wsgi-reload

update-test:
	dropdb timtec-test
	createdb timtec-test
	pg_restore -O -x -n public -d timtec-test ~hacklab/sql-backup/last.psqlc
	cp timtec/settings_local_test.py timtec/settings_local.py
	~/env/bin/pip install -r requirements.txt
	~/env/bin/python manage.py syncdb --noinput
	~/env/bin/python manage.py migrate --noinput
	~/env/bin/python manage.py collectstatic --noinput
	~/env/bin/python manage.py compilemessages
	rm -rf ~/webfiles/media/
	cp -r ~timtec-production/webfiles/media ~/webfiles/
	touch ~/wsgi-reload

update-dev:
	dropdb timtec-dev
	createdb timtec-dev
	pg_restore -O -x -n public -d timtec-dev ~hacklab/sql-backup/last.psqlc
	cp timtec/settings_local_timtec_dev.py timtec/settings_local.py
	~/env/bin/pip install -r requirements.txt
	~/env/bin/python manage.py syncdb --noinput
	~/env/bin/python manage.py migrate --noinput
	~/env/bin/python manage.py collectstatic --noinput -c
	~/env/bin/python manage.py compilemessages
	rm -rf ~/webfiles/media/
	cp -r ~timtec-production/webfiles/media ~/webfiles/
	touch ~/wsgi-reload

update-staging:
	dropdb timtec-staging
	createdb timtec-staging
	pg_restore -O -x -n public -d timtec-staging ~hacklab/sql-backup/last.psqlc
	cp timtec/settings_local_staging.py timtec/settings_local.py
	~/env/bin/pip install -r requirements.txt
	~/env/bin/python manage.py syncdb --noinput
	~/env/bin/python manage.py migrate --noinput
	~/env/bin/python manage.py collectstatic --noinput
	~/env/bin/python manage.py compilemessages
	rm -rf ~/webfiles/media/
	cp -r ~timtec-production/webfiles/media ~/webfiles/
	touch ~/wsgi-reload

update-design:
	cp timtec/settings_local_design.py timtec/settings_local.py
	~/env/bin/pip install -r requirements.txt
	~/env/bin/python manage.py syncdb --noinput
	~/env/bin/python manage.py migrate --noinput
	~/env/bin/python manage.py collectstatic --noinput
	~/env/bin/python manage.py compilemessages
	rm -rf ~/webfiles/media/
	cp -r ~timtec-production/webfiles/media ~/webfiles/
	touch ~/wsgi-reload

staging: create-staging update-staging

update-production:
	cp timtec/settings_local_production.py timtec/settings_local.py
	~/env/bin/pip install -r requirements.txt
	~/env/bin/python manage.py syncdb --noinput
	~/env/bin/python manage.py migrate --noinput
	~/env/bin/python manage.py collectstatic --noinput
	~/env/bin/python manage.py compilemessages
	cp ../settings_production.py timtec/settings_production.py
	touch ~/wsgi-reload

test_collectstatic: clean
	python manage.py collectstatic --noinput -n

clean:
	find . -type f -name '*.py[co]' -exec rm {} \;

python_tests: clean
	py.test --pep8 --flakes --tb=native --reuse-db --cov . . $*

js_tests:
	find . -path ./bower_components -prune -o -path bower_components/ -prune -o -path ./node_modules -prune -o -regex ".*/vendor/.*" -prune -o -name '*.js' -exec jshint {} \;

karma_tests:
	karma start confkarma.js $*

all_tests: clean test_collectstatic python_tests karma_tests js_tests

setup_ci:
	psql -c 'create database timtec_ci;' -U postgres

setup_py:
	pip install -q -r requirements.txt
	pip install -q -r dev-requirements.txt
	python setup.py -q develop

setup_coveralls:
	pip install -q coveralls

setup_js:
	sudo `which npm` -g install less yuglify karma karma-cli karma-phantomjs-launcher karma-jasmine jshint ngmin grunt-cli --loglevel silent
	sudo npm install grunt grunt-angular-gettext

setup_django: clean
	python manage.py syncdb --all --noinput
	python manage.py compilemessages

settings_ci:
	cp timtec/settings_local_ci.py timtec/settings_local.py

dumpdata: clean
	python manage.py dumpdata --indent=2 -n -e south.migrationhistory -e admin.logentry -e socialaccount.socialaccount -e socialaccount.socialapp -e sessions.session -e contenttypes.contenttype -e auth.permission -e account.emailconfirmation -e socialaccount.socialtoken

reset_db: clean
	python manage.py reset_db --router=default --noinput -U $(USER)
	python manage.py syncdb --all --noinput
	python manage.py migrate --noinput --fake

messages: clean
	python manage.py makemessages -a -d django
