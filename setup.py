import os

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = ''

requires = [
    'django',
]

setup(name='timtec',
      version='0.0',
      description='timtec',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Django",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Hacklab',
      author_email='contato@hacklab.com.br',
      url='hacklab.com.br',
      keywords='web wsgi django',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='timtec',
      tests_require=['pytest'],
      cmdclass={'test': PyTest},
      install_requires=requires,
      )
