=======
Hydropy
=======

.. image:: https://img.shields.io/pypi/v/hydropy.svg
        :target: https://pypi.python.org/pypi/hydropy
        :alt: Pypi

.. image:: https://img.shields.io/travis/stijnvanhoey/hydropy.svg
        :target: https://travis-ci.org/stijnvanhoey/hydropy
        :alt: Build Status

.. image:: https://img.shields.io/badge/License-BSD%202--Clause-blue.svg
        :target: https://opensource.org/licenses/BSD-2-Clause
        :alt: BSD-2-Clause

Analysis of hydrological oriented time series.

This package is designed to simplify the collection and analysis of
hydrology data.  Use HydroPy in a Jupyter notebook and save your 
analysis so that you can recreate your procedures and share them with others.  

Hydropy uses the power of Numpy and Pandas to quickly process large datasets. 
Matplotlib and Seaborn are built-in to Hydropy, allowing you to create
publication-ready diagrams quickly and easily.

Try Hydropy in a notebook: `hydropy_tutorial.ipynb`_
.. _`hydropy_tutorial.ipynb`: https://github.com/stijnvanhoey/hydropy/blob/master/hydropy_tutorial.ipynb

Example:
--------

.. code-block:: python

    # Recession periods in June 2011:
    myflowserie.get_year('2011').get_month("Jun").get_recess()

.. image:: ./data/recession.png
        :alt: Recession periods

::

    # Peak values above 90th percentile for station LS06_347 in july 2010:
    myflowserie['LS06_347'].get_year('2010').get_month("Jul").get_highpeaks(150, above_percentile=0.9)


.. image:: ./data/peaks.png
        :alt: Selected peaks

::

    # Select 3 storms out of the series
    storms = myflowserie.derive_storms(raindata['P06_014'], 'LS06_347', number_of_storms=3, drywindow=96, makeplot=True)


.. image:: ./data/storms.png
        :alt: Selected storms

A more extended tutorial/introduction is provided in a ipython notebook: `hydropy_tutorial.ipynb`_

.. `hydropy_tutorial.ipynb`_: https://github.com/stijnvanhoey/hydropy/blob/master/hydropy_tutorial.ipynb

We acknowledge the Flemish Environmental Agency (VMM) for the data used in the tutorial. It can be downloaded from `http://www.waterinfo.be/`_.

.. http://www.waterinfo.be/_: http://www.waterinfo.be/

To install this, git clone the repo and then install it by::

    python setup.py install

To test the functionalities yourself without installing it, use the following environment provided by Binder:

.. image:: http://mybinder.org/badge.svg
        :target: http://mybinder.org/repo/stijnvanhoey/hydropy
        :alt: Binder

Inspiration or possible useful extensions:

* Basically this is a restart of hydropy https://code.google.com/p/hydropy/
* Hydroclimpy http://hydroclimpy.sourceforge.net/
* Georgakakos2004, ROC
* http://cran.r-project.org/web/packages/hydroTSM/vignettes/hydroTSM_Vignette.pdf

The slides version of the notebook was made with nbconvert (using reveal.js), by following command::

    ipython nbconvert hydropy_tutorial.ipynb --to=slides --post=serve --reveal-prefix=reveal.js --config slides_config.py

http://nbviewer.ipython.org/format/slides/github/stijnvanhoey/hydropy/blob/master/hydropy_tutorial.ipynb#/


Copyright (c) 2015-2017 Stijn Van Hoey, Martin Roberge, and Contributors
