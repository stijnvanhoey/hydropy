# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:09:11 2016

@author: Marty
"""

from __future__ import absolute_import, print_function
import pandas as pd

import hydropy as hp


class Analysis(object):
    """holds data for multiple Stations.

    TODO: Structure
        * a start date
        * an end date
        * station_list, a list of at least one Station object
        * a dailymean panel
        * a realtime panel
          TODO: a peak discharge panel
        * panel structure:
            * axis 0 (items): Each item is a dataframe for a site.
            * axis 1 (major_axis / index / rows): uses a datetime index.
            * axis 2 (minor_axis / columns): each column represents a different
                kind of value. the first is Q, or discharge, also Qbf,
                Qquickflow, precip...
          TODO: a site analysis dataframe. Each row is a site, each column
              is some watershed variable or global variable...

    TODO: Behavior
        * Can init with as little as a list of sites.
            * distant future TODO: init with no sites, select from map or list
        * If no start or end specified, and no data exists, then a warning is
            printed.
        * __init__() creates new Stations (these do most of the work)
        * data from Stations gets pulled out into panels for further analysis.
        * all work takes place on the panels.
    """

    def __init__(self, sites, series=None, start=None,
                 end=None, period=None, **kwargs):
        """
        Initialize with a list of sites and their source, or a dataframe.

        Arguments
        ---------
            sites: a list of site ids
            series: ('dailymean' | 'realtime'): the frequency of time sample
                and the type of value.
                'dailymean': average discharge per second for a 24 hour period.
                'realtime': instantaneous value for discharge; sampled <= 1 hr
            source: ('usgs' | 'vmm') the data source.
            start (str): a start date given in the format 'yyyy-mm-dd'
            end (str): an end date given in the format 'yyyy-mm-dd'

        Returns
        -------
            self

        Raises
        ------
            HydroSourceError: when a source that has not been implemented is
                requested.

        Example
        -------
        Create a new Analysis object by passing a list of sites:

        >>> my_study = hp.Analysis(['usgs01585200', 'usgs01582500'],
                                   series='dailymean',
                                   start='2011-04-01',
                                   end='2011-10-01')

        Create a new Analysis object by passing a list of dictionaries that
        specify the site id and the data source:

        >>> sites = [{site: '01585200', source: 'usgs-dv'},
                     {site: '01582500', source: 'usgs-iv'}]
        >>> study2 = hp.Analysis(sites)

        """
        self.station_list = []
        # self.df_dict = {}
        # self.panel = None
        self.start = start
        self.end = end
        self.period = period

        if self.start is None:
            print('A start date must be supplied for this analysis.')
            self.start = '2015-06-01'
        if self.end is None:
            self.end = '2016-06-01'
        # TODO create an Analysis object from a panel.
        # if isinstance(data, pd.Panel):
        #     TODO: Creating an Analysis object directly from a panel will
        #     cause some problems later on. Normally, an Analysis object should
        #     be created out of Station objects, which will handle saving data
        #     and handling metadata. This bypasses that functionality, so how
        #     will that functionality be included?
        #     self.create_panel(data)
        #     self.stations = list(self.panel.items)
        #     if source is None:
        #         print("please set the source for the dataset.")

        # allow single site to be provided without a list.
        if isinstance(sites, str):
            item = sites
            sites = []
            sites.append(item)
        if isinstance(sites, list):
            for site in sites:
                try:
                    site, source = hp.reading_third_party_data.site_parser(site)
                except hp.exceptions.HydroSourceError as e:
                    print(e)
                    # if the source is bad, skip to next on list.
                    continue
                new_station = hp.Station(site,
                                         series=series,
                                         source=source,
                                         start=self.start,
                                         end=self.end,
                                         period=period)
                # call new_station.fetch(site, source, start=start, end=end)
                self.station_list.append(new_station)
            # self.create_panel(self.df_dict)

        # TODO: dealing with a dictionary as input.
        # elif isinstance(sites, dict):
        #    pass

#    def create_panel(self, data):
#        """create a panel from a dictionary of dataframes.

#        arguments:
#        ---------
#            data (pd.Panel): a pandas Panel, with each station as an item
#                holding a dataframe.
#            data (dict): a dict that uses the site_id as the key, and the
#                dataframe from that station as the value.
#        returns:
#        -------
#            self
#        """
#        if isinstance(data, pd.Panel):
#            self.panel = data
#        elif isinstance(data, dict):
#            self.panel = pd.Panel(data)
#        else:
#            raise hp.HydroTypeError("Data of type {0} was supplied to a method"
#                                    " that only accepts type pd.Dataframe or"
#                                    " dict."
#                                    .format(type(data)))
#        return self
