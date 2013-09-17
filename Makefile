
create-staging:
	virtualenv ~/env
	~/env/bin/pip install -r requirements.txt
	mkdir ~/webfiles/static
	mkdir ~/webfiles/media

update-staging:
	cp timtec/settings_local_staging.py timtec/settings_local.py
	~/env/bin/pip install -r requirements.txt
	~/env/bin/python manage.py syncdb --noinput
	~/env/bin/python manage.py collectstatic --noinput
	~/env/bin/python manage.py compilemessages
	touch timtec/wsgi.py

staging: create-staging update-staging

