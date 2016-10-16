from __future__ import absolute_import, print_function

"""
# Hydropy

Analysis of hydrological oriented time series.

This package is especially designed to simplify the collection and analysis of
hydrology data in an interpretive Python session.  Use HydroPy in a Jupyter
notebook and save your analysis so that you can recreate your procedures and
share them with others.

Hydropy uses the power of Numpy and Pandas to quickly process large datasets.

Matplotlib and Seaborn are built-in to Hydropy, allowing you to create
publication-ready diagrams quickly and easily.

Try Hydropy in a notebook: hydropy_tutorial.ipynb

Hydropy is available through [Github](https://github.com/stijnvanhoey/hydropy)
and [PyPI](https://pypi.python.org/pypi/hydropy). The easiest way to use it is
with the Anaconda scientific distribution. If you have Anaconda, or if you
already have numpy, pandas, and matplotlib installed, then use Pip to install
hydropy like this::

    $ pip install hydropy

## Basic Usage::

    >>> import numpy as np
    >>> import pandas as pd

    >>> import hydropy as hp
    >>> flowdata = pd.read_pickle("./data/FlowData")
    >>> flowdata.head()

    >>> myflowserie = hp.HydroAnalysis(flowdata)
    >>> myflowserie.get_year('2009').get_season('summer').plot(figsize=(12,6))

"""

from .baseflow import (get_baseflow_chapman,
                       get_baseflow_boughton,
                       get_baseflow_ihacres)
from .storm import selectstorms, plotstorms
from .flowanalysis import HydroAnalysis
from .reading_third_party_data import get_usgs
from .composition import Station, Analysis
from .exceptions import HydroNoDataError, HydroSourceError

__license__ = 'BSD'
__title__ = 'hydropy'
