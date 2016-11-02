# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 13:08:37 2016

@author: Marty

This module holds the unit tests for station.py and the Station class.
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

class TestStation(unittest.TestCase):

    def test_Station_inits_site(self):
        actual = hp.Station('usgs01585200')
        expected = 'usgs01585200'
        self.assertEqual(expected, actual.site)

    def test_Station_raises_HydroSourceError_no_source(self):
        with self.assertRaises(hp.HydroSourceError):
            actual = hp.Station('01585200')
            actual.fetch()

    def test_Station_raises_HydroSourceError_for_bad_source(self):
        with self.assertRaises(hp.HydroSourceError):
            actual = hp.Station('01585200')
            actual.fetch(source='nonsense')

    def test_Station_str_returns_str(self):
        actual = hp.Station('usgs01585200')
        # This might be a dumb test, because I think an error gets thrown if
        # a __str__ function doesn't return a string.  Hmmm.
        self.assertIsInstance(actual.__repr__(), str)

    def test_Station_repr_returns_str(self):
        actual = hp.Station('usgs01585200')
        self.assertIsInstance(actual.__repr__(), str)

    @unittest.skip("Removed _html_repr_ for Station. Do I want one?")
    def test_Station_htmlrepr_returns_html(self):
        actual = hp.Station('usgs01585200')
        # IPython will take advantage of this function if it exists; The
        # purpose is to display a table of data as html instead of as a string.
        self.assertIsInstance(actual._repr_html_(), str)
        # perhaps it also makes sense to do a regex to check for proper html?

    @mock.patch('hydropy.HydroAnalysis')
    @mock.patch('hydropy.get_usgs')
    def test_Station_fetch_accepts_usgs_realtime(self, mock_get, mock_HA):
        expected = 'mock data'
        mock_get.return_value = expected
        mock_HA.return_value = expected
        start = '2011-01-01'
        end = '2011-01-02'

        actual = hp.Station('usgs01585200')
        actual.fetch(series='realtime', start=start, end=end)

        mock_get.assert_called_once_with('01585200', 'iv', start, end)
        mock_HA.assert_called_once_with(expected)
        self.assertEqual(expected, actual.realtime)

    @mock.patch('hydropy.HydroAnalysis')
    @mock.patch('hydropy.get_usgs')
    def test_Station_fetch_accepts_usgs_dailymean(self, mock_get, mock_HA):
        expected = 'mock data'
        mock_get.return_value = expected
        mock_HA.return_value = expected
        start = '2011-01-01'
        end = '2011-01-02'

        actual = hp.Station('usgs01585200')
        actual.fetch(series='dailymean', start=start, end=end)

        mock_get.assert_called_once_with('01585200', 'dv', start, end)
        mock_HA.assert_called_once_with(expected)
        self.assertEqual(expected, actual.dailymean)
