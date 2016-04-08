# Configuration

## Initial Data
In order to load the initial data for the application, you must execute the following command on Timtec’s root directory, with the virtual environment up and running:

    ./manage.py loaddata initial

Then, to define an administrator’s password, execute:

    ./manage.py changepassword admin

Now, it is possible to access django’s administrator interface at /django/admin.

## Variables
TIM Tec’s configuration is made defining variables on [django’s settings](https://docs.djangoproject.com/en/1.6/ref/settings/) module, using settings_production.py file. Please avoid keeping that file in the repository’s directory, otherwise every source code update will overwrite it.  
All relevant configuration variables have been isolated in this python module, in order to simplify the configuration process, because django’s settings module also defines project specific information, for instance, django’s apps used by the project.  
First, activated the virtual environment:

    source /env/bin/activate

After any change made to settings_production.py file, the following command should be executed on TIM Tec’s root directory, with the virtual environment activated, in order to apply the changes.

    make update-production

For advanced users, settings.py file contains most of the definitions for TIM Tec’s application. It can be found inside the root repository directory at timtec/settings.py.  
The following sections describe each configuration’s variable.

## Theme
Define a Theme for TIM Tec. There are, currently, three possible themes:

* **default**: a neutral theme, a default theme for the software.
* **timtec**: this theme can be seen at: [timtec.com.br](http://timtec.com.br/)
* **ifsul**: developed for Instituto Federal de Educação, Ciência e Tecnologia.

It is possible to set any of the three values above on TIMTEC_THEME variable, for instance:

    TIMTEC_THEME = 'default'

## Authentication
Authentication is implemented using django-allauth, and it has a few configuration variables too. Django-allauth is used to configure login and authentication using Facebook.  
For more information about supported configuration variables:  

[https://readthedocs.org/projects/django-allauth/](https://readthedocs.org/projects/django-allauth/).

To enable and configure Facebook authentication, it is necessary to create an app for Facebook, using the following documentation:  
[https://developers.facebook.com/docs/javascript](https://developers.facebook.com/docs/javascript).

## Allowed Hosts
The [ALLOWED_HOSTS](https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts) variable defines from which domains the application will accept connections (requests):

    ALLOWED_HOSTS = [ 'localhost', 'timtec.com.br', '.timtec.com.br', ]

## Email Configuration
These configurations are defined by [EMAIL_BACKEND](https://docs.djangoproject.com/en/1.6/ref/settings/#email-backend) variable. For more information, refer to django’s official documentation about emails:   
[https://docs.djangoproject.com/en/1.6/topics/email/#email-backends](https://docs.djangoproject.com/en/1.6/topics/email/#email-backends)
It is important to keep in mind that if the email configuration is incorrect, user creation from the application will fail.
