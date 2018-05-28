# Hydropy

[![Pypi](https://img.shields.io/pypi/v/hydropy.svg)](https://pypi.python.org/pypi/hydropy) [![Build Status](https://img.shields.io/travis/stijnvanhoey/hydropy.svg)](https://travis-ci.org/stijnvanhoey/hydropy) [![License](https://img.shields.io/badge/License-BSD%202--Clause-blue.svg)](https://opensource.org/licenses/BSD-2-Clause)

Analysis of hydrological oriented time series.

This package is designed to simplify the collection and analysis of hydrology data. Use HydroPy in a Jupyter notebook and save your analysis so that you can recreate your procedures and share them with others.  

Hydropy uses the power of Numpy and Pandas to quickly process large datasets. Matplotlib and Seaborn are built-in to Hydropy, allowing you to create publication-ready diagrams quickly and easily.

Try Hydropy in a notebook: [hydropy_tutorial.ipynb](https://github.com/stijnvanhoey/hydropy/blob/master/hydropy_tutorial.ipynb)

## Example:

```python
# Recession periods in June 2011:
myflowserie.get_year('2011').get_month("Jun").get_recess()
```

![Recession periods](./data/recession.png)

```python
# Peak values above 90th percentile for station LS06_347 in july 2010:
myflowserie['LS06_347'].get_year('2010').get_month("Jul").get_highpeaks(150, above_percentile=0.9)
```

![Selected peaks](./data/peaks.png)

```python
# Select 3 storms out of the series
storms = myflowserie.derive_storms(raindata['P06_014'], 'LS06_347', number_of_storms=3, drywindow=96, makeplot=True)
```

![Selected storms](./data/storms.png)

A more extended tutorial/introduction is provided in a ipython notebook: [hydropy_tutorial.ipynb](https://github.com/stijnvanhoey/hydropy/blob/master/hydropy_tutorial.ipynb)

We acknowledge the Flemish Environmental Agency (VMM) for the data used in the tutorial. It can be downloaded from http://www.waterinfo.be/.

To install this, git clone the repo and then install it by:

    python setup.py install

To test the functionalities yourself without installing it, use following test environment provided by Binder: [![Binder](http://mybinder.org/badge.svg)](http://mybinder.org/repo/stijnvanhoey/hydropy)

Inspiration or possible useful extensions:

* Basically this is a restart of hydropy https://code.google.com/p/hydropy/
* Hydroclimpy http://hydroclimpy.sourceforge.net/
* Georgakakos2004, ROC
* http://cran.r-project.org/web/packages/hydroTSM/vignettes/hydroTSM_Vignette.pdf

The slides version of the notebook was made with nbconvert (using reveal.js), by following command:

    ipython nbconvert hydropy_tutorial.ipynb --to=slides --post=serve --reveal-prefix=reveal.js --config slides_config.py

http://nbviewer.jupyter.org/format/slides/github/stijnvanhoey/hydropy/blob/master/hydropy_tutorial.ipynb

Copyright (c) 2015-2017 Stijn Van Hoey, Martin Roberge, and Contributors
