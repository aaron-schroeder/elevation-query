# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


pkg_name = 'query'


def read(rel_path):
  """Read a file so python does not have to import it.
  
  Inspired by (taken from) pip's `setup.py`.
  """
  here = os.path.abspath(os.path.dirname(__file__))
  # intentionally *not* adding an encoding option to open, See:
  #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
  with open(os.path.join(here, rel_path), 'r') as fp:
    return fp.read()


def get_version(rel_path):
  """Manually read through a file to retrieve its `__version__`.
  
  Inspired by (taken from) pip's `setup.py`.
  """
  for line in read(rel_path).splitlines():
    if line.startswith('__version__'):
      # __version__ = '0.0.1'
      delim = "'" if "'" in line else '"'
      return line.split(delim)[1]
  raise RuntimeError('Unable to find version string.')


with open('README.md') as f:
  readme = f.read()

with open('LICENSE') as f:
  license = f.read()

setup(
  name=pkg_name,
  version=get_version('%s/__init__.py' % pkg_name),
  description='Python library for getting elevation data from GPS coordinates',
  long_description=readme,
  long_description_content_type='text/markdown',
  author='Aaron Schroeder',
  #author_email='',
  install_requires = [
    'requests>=2.25.1',
  ],
  extras_require={
    'local': ['rasterio==1.1.8', 'pyproj==3.0.0', 'numpy>=1.15',],
    'google': ['googlemaps>=3.0', 'numpy>=1.15',],
  },
  url='https://github.com/aaron-schroeder/elevation-query',
  license=license,
  packages=find_packages(exclude=('tests', 'docs')),
  classifiers=[
    #'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: MIT License',
  ],
)


# Spatialfriend stuff
# requirements = ['geopy>=1.20.0', 'googlemaps>=3.0', 'numpy>=1.14',
#                 'pandas>=0.24', 'scipy>=1.1']

# setup(name='spatialfriend',
#       version='0.0.11',
#       author='Aaron Schroeder',
#       author_email='aaron@trailzealot.com',
#       description='Python library for calculating geospatial data'  \
#                 + ' from gps coordinates.',
#       long_description=readme,
#       long_description_content_type='text/markdown',
#       url='https://github.com/aaron-schroeder/spatialfriend',
#       packages=['spatialfriend'],
#       install_requires=requirements,
#       extras_require={
#         'local': ['rasterio==1.1.8', pyproj==3.0.0, 'numpy>=1.15',],
#         'google', ['googlemaps>=3.0']
#       },
#       license='MIT License',
#       classifiers=['Programming Language :: Python :: 3.6',
#                    'License :: OSI Approved :: MIT License',],)