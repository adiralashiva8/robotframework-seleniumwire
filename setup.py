import sys
from os.path import abspath, dirname, join

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


PY3 = sys.version_info > (3,)

VERSION = None
version_file = join(dirname(abspath(__file__)), 'src', 'SeleniumWireLibrary', 'version.py')
with open(version_file) as file:
    code = compile(file.read(), version_file, 'exec')
    exec(code)

DESCRIPTION = """
Robot Framework keyword library wrapper around the selenium-wire library.
"""[1:-1]

CLASSIFIERS = """
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]


setup(
      name='robotframework-seleniumwire',
      version=VERSION,
      description='Robot Framework keyword library wrapper around selenium-wire library',
      long_description=DESCRIPTION,
      author='Shiva Adirala',
      author_email='adiralashiva8@gmail.com',
      url='https://github.com/adiralashiva8/robotframework-seleniumwire',
      license='MIT',
      keywords='robotframework testing automation selenium-wire',
      platforms='any',
      classifiers=CLASSIFIERS.splitlines(),
      package_dir={'': 'src'},
      packages=['SeleniumWireLibrary'],
      install_requires=[
          'robotframework',
          'selenium',
          'selenium-wire',
      ],)