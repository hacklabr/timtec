import tempfile
import pytest
from django.conf import settings
from django.core.management import call_command


@pytest.mark.skipif('not pytest.config.getvalue("collectstatic")')
def test_collectstaticworking():
    tempdir = tempfile.mkdtemp()
    settings.STATIC_ROOT = tempdir
    print 'running collectstatic to', tempdir
    call_command('collectstatic', interactive=False)
