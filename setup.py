#!/usr/bin/env python

from setuptools import setup

setup(name='hydropy',
      version='0.1',
      description='Analysis of hydrological oriented time series',
      url='https://stijnvanhoey.github.io/hydropy/',
      author='Stijn Van Hoey',
      author_email='stvhoey.vanhoey@ugent.be',
      license='BSD',
      include_package_data=True,
      install_requires=['scipy', 'numpy', 'pandas', 'matplotlib', 'seaborn',
                        'requests'],
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
