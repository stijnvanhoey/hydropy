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
        actual = hp.Station('any')
        expected = 'any'
        self.assertEqual(expected, actual.site)

    def test_Station_raises_HydroSourceError_no_source(self):
        actual = hp.Station('any')
        with self.assertRaises(hp.HydroSourceError):
            actual.fetch()

    def test_Station_raises_HydroSourceError_for_bad_source(self):
        with self.assertRaises(hp.HydroSourceError):
            actual = hp.Station("any")
            actual.fetch(source='nonsense')

    def test_Station_str_returns_str(self):
        actual = hp.Station('any')
        # This might be a dumb test, because I think an error gets thrown if
        # a __str__ function doesn't return a string.  Hmmm.
        self.assertIsInstance(actual.__repr__(), str)

    def test_Station_repr_returns_str(self):
        actual = hp.Station('any')
        self.assertIsInstance(actual.__repr__(), str)

    @unittest.skip("Removed _html_repr_ for Station. Do I want one?")
    def test_Station_htmlrepr_returns_html(self):
        actual = hp.Station('any')
        # IPython will take advantage of this function if it exists; The
        # purpose is to display a table of data as html instead of as a string.
        self.assertIsInstance(actual._repr_html_(), str)
        # perhaps it also makes sense to do a regex to check for proper html?

    @mock.patch('hydropy.HydroAnalysis')
    @mock.patch('hydropy.get_usgs')
    def test_Station_fetch_accepts_source_usgs_iv(self, mock_get, mock_HA):
        expected = 'mock data'
        mock_get.return_value = expected
        mock_HA.return_value = expected

        actual = hp.Station('usgs01585200')
        actual.fetch(source='usgs-iv', start='A', end='B')

        mock_get.assert_called_once_with('01585200', 'iv', 'A', 'B')
        mock_HA.assert_called_once_with(expected)
        self.assertEqual(expected, actual.realtime)

    @mock.patch('hydropy.HydroAnalysis')
    @mock.patch('hydropy.get_usgs')
    def test_Station_fetch_accepts_source_usgs_dv(self, mock_get, mock_HA):
        expected = 'mock data'
        mock_get.return_value = expected
        mock_HA.return_value = expected

        actual = hp.Station('usgs01585200')
        actual.fetch(source='usgs-dv', start='A', end='B')

        mock_get.assert_called_once_with('01585200', 'dv', 'A', 'B')
        mock_HA.assert_called_once_with(expected)
        self.assertEqual(expected, actual.dailymean)