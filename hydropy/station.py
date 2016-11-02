# -*- coding: utf-8 -*-
"""
station.py

This module defines the Station class and its methods. test_station.py tests
this module.
"""
from __future__ import absolute_import, print_function
import pandas as pd

import hydropy as hp


class Station(object):
    """Holds data for a single stream gauge or precipitation gauge.

    TODO: Start simple. Create methods to populate the new Station with a
        dataframe, and a method to populate the new Station with data requested
        from a source. Later, add logic that allows these functions to be
        called from inside the __init__().

    TODO: Behavior:
        Initialize with as little as a site ID.
        INIT will check for saved files for this site
            if a file exists, it will return with a description of what data
            exists in the file: dailymean, realtime, start, end
        INIT will check if a start or end parameter has been specified, and
            will request additional data if start is earlier or end is later
            than what might be in the datafile.
        If no start, end, or period set, init will finish.
            Maybe provide a warning that no date selected?
            
        Whenever data is requested, it gets added to whatever already exists
            and saved to disk.
        

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

    def __init__(self, site, source=None, series=None,
                 start=None, end=None, period=None):
        """Initialize the Station object by giving it an id that is derived
        from the id of the physical station site that is collecting the data.
        Save the **kwargs to the Station object.

        Example:
        --------
        >>> new_station = hp.Station('usgs01585200')

        Example (future usage):
        -----------------------
        >>> newDF = pd.DataFrame(np.random.randn(10, 5))
        >>> newStation = hp.Station(newDF)

        >>> new_data = np.random.randn(10, 5)
        >>> newStation2 = hp.Station(new_data, columns=['a', 'b', 'c', 'd', 'e']))

        >>> newStation3 = hp.Station(['usgs01585200', 'usgs01581500'])
        """
        # TODO: check if there is another object with the same site id.
        # TODO: check if there is any data for this site saved to disk.

        self.site, self.source = hp.reading_third_party_data.site_parser(site)

        if series is None:
            self.series = 'dailymean'
        else:
            self.series = series

        self.start = start
        self.end = end
        self.period = period
        self.dailymean = None
        self.realtime = None

    def fetch(self, series=None, source=None, start=None, end=None,
              period=1, **kwargs):
        """Retrieve data from a source.

        For now, use source as a switch to call a retrieval function. In the
        future, maybe set the fetch function when the object is initialized and
        then call it.

        Arguments:
        ---------
            source ('usgs' | 'vmm'): the data source.

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

        >>> HerringRun = Station('usgs01585200')
        >>> HerringRun.fetch()

        Fetches the past 1 day of values.

        >>> StonyRun = Station('usgs01589464')
        >>> StonyRun.fetch(series='realtime', start='2014-06-01',
                           end='2014-06-04')

        Fetches instantaneous values with a collection interval of 15 minutes
        for June 1-4, 2014.
        """
        if start is not None:
            # TODO: only alter self.start if start is earlier.
            self.start = start
        if end is not None:
            # TODO only alter self.end if end is later.
            self.end = end
        if period is not None:
            # not implemented yet.
            self.period = period
        if series is None:
            series = 'dailymean'

        if self.source is None:
            if source is None:
                raise hp.HydroSourceError("No source was defined for this "
                                          ".fetch() request. To set a source, "
                                          "use .fetch(source='usgs') or "
                                          "another source, such as 'vmm'.")
            else:
                self.source = source

        if self.source == 'usgs':
            usgs_id = self.site[4:]
            if series == 'dailymean':
                # Save to dailymean as a HydroAnalysis object.
                df = hp.get_usgs(usgs_id, 'dv', self.start, self.end)
                self.dailymean = hp.HydroAnalysis(df)
            elif series == 'realtime':
                # retrieve usgs iv data. Save to realtime.
                df = hp.get_usgs(usgs_id, 'iv', self.start, self.end)
                self.realtime = hp.HydroAnalysis(df)
            else:
                raise hp.HydroSourceError('The series {0} is not recognized.')
        else:
            raise hp.HydroSourceError('The source {0} is not defined.'
                                      .format(self.source))

        return self

#    def pandas(self, data, **kwargs):
#        """Create a station object using the pandas constructor.
#
#                 data=None, # create a dataframe through Pandas.
#                 index=None, # Pandas uses this to create a dataframe.
#                 site=None, # use to identify this Station.
#                 source=None, # Needed to collect data
#                 start=None,
#                 end=None,
#                 period=None,
#                 **kwargs):
#        Initialize a new Station object.
#
#        You can create a new station by passing in a new dataframe or by
#        specifying the source and site id.
#        """
#
#        # if data is None,
#        if data is None:
#            # use the other arguments to retrieve data from a source.
#            pass
#        if isinstance(data, pd.DataFrame):
#            # they sent us a dataframe. I guess there ain't much to do...?
#            # or send this dataframe to pandas.dataframe constructor.
#            pass
#        else:
#            # Send data to Pandas; maybe it will create a dataframe for us.
#            # try:  #Maybe don't catch this error? is the message good enough?
#            # Pandas accepts
#            pass
