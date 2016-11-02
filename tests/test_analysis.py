# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 23:30:01 2016

@author: Marty
"""
from __future__ import absolute_import, print_function

try:
    from unittest import mock
except ImportError:
    import mock
import unittest

import numpy as np
import pandas as pd
import hydropy as hp


class TestAnalysis(unittest.TestCase):

    def test_Analysis_accepts_single_site(self):
        actual = hp.Analysis('usgs01585200',
                             series='dailymean',
                             start='2011-05-01',
                             end='2011-05-01')
        # Check that actual changes Stations from None to a list.
        self.assertIsNotNone(actual.station_list)
        self.assertIsInstance(actual.station_list, list)
        # Check that each element of the list is a Station.
        self.assertEqual(len(actual.station_list), 1)
        self.assertIsInstance(actual.station_list[0], hp.Station)

    def test_Analysis_accepts_list_dailymean(self):
        actual = hp.Analysis(['usgs01585200', 'usgs01581500'],
                             series='dailymean',
                             start='2011-05-01',
                             end='2011-05-01')
        # Check that actual changes Stations from None to a list.
        self.assertIsNotNone(actual.station_list)
        self.assertIsInstance(actual.station_list, list)
        # Check that each element of the list is a Station.
        self.assertEqual(len(actual.station_list), 2)
        self.assertIsInstance(actual.station_list[0], hp.Station)

    def test_Analysis_accepts_list_realtime(self):
        actual = hp.Analysis(['usgs01585200', 'usgs01581500'],
                             series='realtime',
                             start='2011-05-01',
                             end='2011-05-01')
        # Check that actual changes Stations from None to a list.
        self.assertIsNotNone(actual.station_list)
        self.assertIsInstance(actual.station_list, list)
        # Check that each element of the list is a Station.
        self.assertEqual(len(actual.station_list), 2)
        self.assertIsInstance(actual.station_list[0], hp.Station)

    @unittest.skip("series='nonsense' isn't evaluated until Station is told to"
                   "fetch().")
    def test_Analysis_raises_HydroSourceError_for_bad_series(self):
        with self.assertRaises(hp.HydroSourceError):
            actual = hp.Analysis(['usgs01585200', 'usgs01581500'],
                                 series='nonsense',
                                 start='2011-05-01',
                                 end='2011-05-01')
            # This could be used to force Stations to fetch.
            # actual.fetch()

    # Future input types dict and panel
    @unittest.skip("Analysis doesn't accept dict yet")
    def test_Analysis_accepts_dict(self):
        actual = hp.Analysis({'blah': 'blah'})
        expected = 'dict'
        self.assertEqual(expected, actual.source)

    @unittest.skip("Analysis doesn't accept Panels yet")
    def test_Analysis_accepts_Panel(self):
        wp = pd.Panel(np.random.randn(2, 5, 4), items=['Item1', 'Item2'],
                      major_axis=pd.date_range('1/1/2000', periods=5),
                      minor_axis=['A', 'B', 'C', 'D'])
        actual = hp.Analysis(wp, source='usgs')
        self.assertListEqual(actual.stations, ['Item1', 'Item2'])

    @unittest.skip("Analysis doesn't accept Panels yet")
    def test_Analysis_create_panel_raises_HydroTypeError_bad_data(self):
        with self.assertRaises(hp.HydroTypeError):
            actual = hp.Analysis('usgs01585200')
            actual.create_panel("invalid input")

    @unittest.skip("Analysis doesn't accept Panels yet")
    def test_Analysis_create_panel_returns_Analysis_self(self):
        newAnalysis = hp.Analysis('usgs01585200')
        wp = pd.Panel(np.random.randn(2, 5, 4), items=['Item1', 'Item2'],
                      major_axis=pd.date_range('1/1/2000', periods=5),
                      minor_axis=['A', 'B', 'C', 'D'])
        actual = newAnalysis.create_panel(wp)
        self.assertIs(newAnalysis, actual)

    @unittest.skip("Analysis doesn't accept Panels yet")
    def test_Analysis_create_panel_accepts_panels(self):
        newAnalysis = hp.Analysis('usgs01585200')
        wp = pd.Panel(np.random.randn(2, 5, 4), items=['Item1', 'Item2'],
                      major_axis=pd.date_range('1/1/2000', periods=5),
                      minor_axis=['A', 'B', 'C', 'D'])
        actual = newAnalysis.create_panel(wp)
        self.assertIsInstance(actual.panel, pd.Panel)

    @unittest.skip("Analysis doesn't accept Panels yet")
    def test_Analysis_create_panel_accepts_dict_of_df(self):
        newAnalysis = hp.Analysis('usgs01585200')
        df1 = pd.DataFrame(np.random.randn(5, 4))
        df2 = pd.DataFrame(np.random.randn(5, 4))
        valid_dict_of_df = {'item1': df1, 'item2': df2}
        actual = newAnalysis.create_panel(valid_dict_of_df)
        self.assertIsInstance(actual.panel, pd.Panel)

    def test_Analysis_behaviors(self):
        pass
        # create an analysis object with a list of valid stations and a source
        # new_study = hp.Analysis(['01585200', '01582500'], source='usgs-dv')

        # Analysis object creates new Station objects...
        # ...and stores them internally.

        # when created, new Station objects will:
        #   record their source
        #   keep a dataframe of data
        #   save different types of data to different dataframes.
        #       types: daily mean values; frequent instantaneous values; peaks
        #   save their data to disk automatically
        #   check for locally saved data before requesting online

        # Accessing data usually occurs through analysis objects
        # new_study.dailymean  produces a panel of dailymeans.
        # new_study.usgs01585200.dailymean produces a df
        # new_study.dailymean.usgs01585200 produces the same df

        # You can run an analysis on an analysis object with just one command.
        # produce a hydrograph of something (seems ambiguous!)
        #   new_study.hydrograph()

        # produces a hydrograph of all of the series combined in one graph:
        #   new_study.dailymean.hydrograph()
        # produce hydrographs for each of the series seperately:
        #   new_study.dailymean.hydrographs()
        #   or
        #   new_study.dailymean.foreach().hydrograph()
        # yikes! I guess foreach() would have to be a generator that spits out
        # station objects or something...

        # smart analysis: flowduration only works on daily mean by default.
        #   new_study.flowduration()
        # smart analysis2: extract_peaks() would only work on instantaneous val
        # smart analysis: 
