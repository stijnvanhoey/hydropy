#!/usr/bin/env python
from __future__ import absolute_import
from setuptools import setup

with open('README.rst') as readme_file:
      readme = readme_file.read()

with open('AUTHORS.rst') as authors_file:
      authors = authors_file.read()

setup(name='hydropy',
      version='0.1.2',
      description='Analysis of hydrological oriented time series',
      long_description=readme + '\n\n' + authors,
      url='https://github.com/stijnvanhoey/hydropy/',
      author='Stijn Van Hoey',
      author_email='stijnvanhoey@gmail.com',
      license='BSD',
      include_package_data=True,
      install_requires=['scipy', 'numpy', 'pandas', 'matplotlib', 'seaborn',
                        'requests', 'IPython'],
      tests_require=['mock'],
      packages=['hydropy'],
      keywords='hydrology time series hydroTSM',
      test_suite='tests',
      classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Utilities'
        ])
