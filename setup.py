#!/usr/bin/env python

from setuptools import setup

setup(name='hydropy',
	  version='0.1',
	  description='Analysis of hydrological oriented time series',
	  url='https://stijnvanhoey.github.io/hydropy/',
      author='Stijn Van Hoey',
	  author_email='stvhoey.vanhoey@ugent.be',
	  #license=' ',
       include_package_data=True,
	  packages=['hydropy'],
	  keywords='hydrology time series hydroTSM',
       classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Utilities'
    ],)
