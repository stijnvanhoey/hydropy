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
        
        Example (future usage):
        -----------------------
        >>> newDF = pd.DataFrame(np.random.randn(10, 5))
        >>> newHdf = hp.Station(newDF)

        >>> new_data = np.random.randn(10, 5)
        >>> newHdf2 = hp.Station(new_data, columns=['a', 'b', 'c', 'd', 'e']))

        >>> newHdf3 = hp.Station(['01585200', '01581500'], source='usgs-dv')
        """
        # TODO: check if there is another object with the same site id.
        # TODO: check if there is any data for this site saved to disk.
        self.site = site
        #self.data is the default data to show for printing or other functions.
        self.data = None
        self.dailymean = None
        self.realtime = None
        self.type = None

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

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)

    def _repr_html_(self):
        """return the data formatted as html in an IPython notebook.
        """
        if self.data is None:
            return "No data for this Station"
        return pd.DataFrame._repr_html_(self.data.data)

    def fetch(self, source='usgs-dv', start=None, end=None,
              period=1, **kwargs):
        """Retrieve data from a source.

        For now, use source as a switch to call a retrieval function. In the
        future, maybe set the fetch function when the object is initialized and
        then call it.

        Arguments:
        ---------
            source ('usgs-iv' | 'usgs-dv'): the data source.

            start (date str): a string to represent the start date. Right now,
                this is just a string that gets passed to the usgs. It should
                take on the form 'yyyy-mm-dd'.

            end (date str): a string to represent the end date. It should
                take on the form 'yyyy-mm-dd'

            period (int): number of days in the past to request data. Not
                implemented yet.

        Returns:
        -------
            self

        Raises:
        ------
            HydroSourceError: when a source that has not been implemented is
                requested.

        Example:
        -------

        >>> HerringRun = Station('01585200')
        >>> HerringRun.fetch()

        Fetches the past 1 day of values.

        >>> StonyRun = Station('01589464')
        >>> StonyRun.fetch(source='usgs-iv', start='2014-06-01',
                           end='2014-06-04')

        Fetches instantaneous values with a collection interval of 15 minutes
        for June 1-4, 2014.
        """
        self.start = start
        self.end = end
        self.period = period

        if source == 'usgs-dv':
            # retrieve usgs data. Save to dailymean as a HydroAnalysis object.
            df = hp.get_usgs(self.site, 'dv', self.start, self.end)
            self.dailymean = hp.HydroAnalysis(df)
            self.type = 'dailymean'
            self.data = self.dailymean
        elif source == 'usgs-iv':
            # retrieve usgs iv data. Save to realtime.
            df = hp.get_usgs(self.site, 'iv', self.start, self.end)
            self.realtime = hp.HydroAnalysis(df)
            self.type = 'realtime'
            self.data = self.realtime
        else:
            raise hp.HydroSourceError('The source {0} is not defined.'
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
    """holds data for multiple Stations.
    """

    def __init__(self, data, source=None, **kwargs):
        """
        Initialize with a list of sites and their source, or a dataframe.

        Arguments
        ---------
            data: a list of site ids
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
        Create a new Analysis object by passing a list of sites and a source:

        >>> my_study = hp.Analysis(['01585200', '01582500'], source='usgs-dv')

        Create a new Analysis object by passing a list of dictionaries that
        specify the site id and the data source:

        >>> sites = [{site: '01585200', source: 'usgs-dv'},
                     {site: '01582500', source: 'usgs-iv'}]
        >>> study2 = hp.Analysis(sites)

        """
        self.stations = []
        self.panel = None
        self.source = source

        # Phase 1: only accept lists & source as arguments.
        #   if source:
        #       categorize source;
        #       for each item in list, make a new Station
        #       append the Station to the list.

        # print('new Analysis object')
        if isinstance(data, pd.Panel):
            # TODO: Creating an Analysis object directly from a panel will
            # cause some problems later on. Normally, an Analysis object should
            # be created out of Station objects, which will handle saving data
            # and handling metadata. This bypasses that functionality, so how
            # will that functionality be included?
            self.create_panel(data)
            self.stations = list(self.panel.items)
            if source is None:
                print("please set the source for the dataset.")
        if isinstance(data, list) and source is not None:
            #print('A')
            if source == 'usgs-dv' or source == 'usgs-iv':
                self.source = source
                #print('B')
                for site in data:
                    new_station = hp.Station(site)
                    new_station.source = source
                    # call new_station.fetch(site, source, start=start, end=end)
                    self.stations.append(new_station)
            else:
                #print('D')
                # Raise an error if an unknown source is given.
                raise hp.HydroSourceError("The {0} service is not implemented"
                                          "yet.".format(source))
        # Phase 2: dealing with a dictionary as input.
        elif isinstance(data, dict):
            self.source = 'dict'

        # print(data)
        # print(source)
        # print(kwargs)

        # If data is passed, like a dict of series, or df
        # self.df = pd.DataFrame(data)
        # accepts data, then index=, columns=,

    def create_panel(self, data):
        """create a panel from a dictionary of dataframes.

        arguments:
        ---------
            data (pd.Panel): a pandas Panel, with each station as an item
                holding a dataframe.
            data (dict): a dict that uses the site_id as the key, and the
                dataframe from that station as the value.
        returns:
        -------
            self
        """
        if isinstance(data, pd.Panel):
            self.panel = data
        elif isinstance(data, dict):
            self.panel = pd.Panel(data)
        else:
            raise hp.HydroTypeError("Data of type {0} was supplied to a method"
                                 " that only accepts type pd.Dataframe or dict"
                                 .format(type(data)))
        return self
