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
        * at least one Station object
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

    def __init__(self, data, source=None, start=None,
                 end=None, period=None, **kwargs):
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
        self.station_list = []
        self.df_dict = {}
        self.panel = None
        self.start = start
        self.end = end
        self.period = period

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
        elif isinstance(data, list) and source is not None:
            if source == 'usgs-dv' or source == 'usgs-iv':
                for site in data:
                    new_station = hp.Station(site, source=source).fetch()
                    self.df_dict[site] = new_station.data.data
                    # call new_station.fetch(site, source, start=start, end=end)
                    self.station_list.append(new_station)
                self.create_panel(self.df_dict)
            else:
                # Raise an error if an unknown source is given.
                raise hp.HydroSourceError("The {0} service is not implemented"
                                          "yet.".format(source))
        # Phase 2: dealing with a dictionary as input.
        elif isinstance(data, dict):
            self.source = 'dict'

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
                                    " that only accepts type pd.Dataframe or"
                                    " dict."
                                    .format(type(data)))
        return self
