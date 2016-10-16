# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:09:11 2016

@author: Marty
"""

from __future__ import absolute_import, print_function
import numpy as np
import pandas as pd

import hydropy as hp


class Station(object):
    """Holds data for a single stream gauge or precipitation gauge.

    TODO: Start simple. Create methods to populate the new Station with a
        dataframe, and a method to populate the new Station with data requested
        from a source. Later, add logic that allows these functions to be
        called from inside the __init__().

    Different types of data get held in different dataframes. Daily mean
    discharge is separated from 15 minute instantaneous data and peak
    instantaneous data. Each series can have derived series that share the same
    time index values in the same dataframe. For example, a daily mean
    discharge may also have an adjacent column for baseflow, quickflow, and
    daily total precipitation.

    Each station object can be created alone by passing a dataframe or by
    passing a site id and a data source at creation. However, new Stations will
    most often be created by an Analysis object.

    The Station class will have some methods associated with it for analysis
    and for saving.  Station.dmd.baseflow() will calculate baseflow for the
    daily mean discharge series; Station.iv.baseflow() will calculate baseflow
    for the instantaneous values.
    """

    def __init__(self, site):
        """Initialize the Station object by giving it an id that is derived
        from the id of the physical station site that is collecting the data.
        Save the **kwargs to the Station object.
        """
        # TODO: check if there is another object with the same site id.
        # TODO: check if there is any data for this site saved to disk.
        self.site = site

        # future:
        # define these here.
        # self.site = site
        # self.source = source
        # self.start = start
        # self.end = end

        # future: pass the fetch function in at initialization.
        # if kwargs.get('fetch'):
        #    self.fetch = fetch
        # elif self.source == 'usgs-iv':
        #    self.fetch = get_usgs(self.site, 'iv', self.start, self.end)
        # elfi self.source == 'usgs-dv':
        #    self.fetch = get_usgs(self.site, 'dv', self.start, self.end)
        # elif self.source is None:
        #   print('Must set source')
        # else:
        #   raise HydroNameError('The source {0} is not defined.'
        #                        .format(source))
        #
        # self.data = self.fetch()

    def fetch(self, source='usgs-dv', start=None, end=None,
              period=180, **kwargs):
        """Retrieve data from a source.

        For now, use source as a switch to call a retrieval function. In the
        future, maybe set the fetch function when the object is initialized and
        then call it.

        Arguments
        ---------
            source: ('usgs-iv' | 'usgs-dv') the data source.

        Returns
        -------
            self

        Raises
        ------
            HydroSourceError: when a source that has not been implemented is
                requested.

        Example
        -------

        >>>
        """
        self.start = start
        self.end = end
        self.period = period

        if source == 'usgs-dv':
            # retrieve usgs data. Save to daily-mean
            self.data = hp.get_usgs(self.site, 'dv', self.start, self.end)
        elif source == 'usgs-iv':
            # retrieve usgs iv data. Save to instantaneous values.
            self.data = hp.get_usgs(self.site, 'iv', self.start, self.end)
        else:
            raise hp.HydroNameError('The source {0} is not defined.'
                                    .format(source))

        return self

    def pandas(self, data, **kwargs):
        """Create a station object using the pandas constructor.

                 data=None, # create a dataframe through Pandas.
                 index=None, # Pandas uses this to create a dataframe.
                 site=None, # use to identify this Station.
                 source=None, # Needed to collect data
                 start=None,
                 end=None,
                 period=None,
                 **kwargs):
        Initialize a new Station object.

        You can create a new station by passing in a new dataframe or by
        specifying the source and site id.
        """

        # if data is None,
        if data is None:
            # use the other arguments to retrieve data from a source.
            pass
        if isinstance(data, pd.DataFrame):
            # they sent us a dataframe. I guess there ain't much to do...?
            # or send this dataframe to pandas.dataframe constructor.
            pass
        else:
            # Send data to Pandas; maybe it will create a dataframe for us.
            # try:  #Maybe don't catch this error? is the message good enough?
            # Pandas accepts
            pass


class Analysis(object):
    """A mega-class to combine the functionality of pandas with special
    hydrology functions.

    """

    def __init__(self, data, source=None, **kwargs):
        """
        pass in a site name, or data.

        Example:
        --------
        >>> newDF = pd.DataFrame(np.random.randn(10, 5))
        >>> newHdf = hp.Hydro(newDF)

        >>> new_data = np.random.randn(10, 5)
        >>> newHdf2 = hp.Hydro(new_data, columns=['a', 'b', 'c', 'd', 'e']))

        >>> newHdf3 = hp.Hydro(['01585200', '01581500'], source='usgs-dv')
        """
        # self.source = source

        print('newish')
        if isinstance(data, list) and source is not None:
            print('A')
            if source == 'usgs-dv':
                print('B')
                for site in data:
                    # call get_usgs and make a new Series.
                    print(site)
                self.source = source
            elif source == 'usgs-iv':
                print('C')
                for site in data:
                    # call get_usgs and make a new Series.
                    print(site)
                self.source = source
            else:
                print('D')
                # Raise an error if an unknown source is given.
                raise hp.HydroSourceError("The {0} service is not implemented"
                                          "yet.".format(source))
        elif isinstance(data, dict):
            self.source = 'dict'



        print(data)
        print(source)
        print(kwargs)

        # If data is passed, like a dict of series, or df
        # self.df = pd.DataFrame(data)
        # accepts data, then index=, columns=,
