# -*- coding: utf-8 -*-
"""
test_baseflow.py
"""

from __future__ import absolute_import, print_function
import unittest

from hydropy import baseflow


class TestBaseflow(unittest.TestCase):

    def test_baseflow_get_bf_chapman_pass(self):
        pass

    def test_baseflow_get_bf_chapman_raises_exception_when_fed_bad_data(self):
        nonsense = "meaningless data"
        # Note: it might make more sense to make this raise a TypeError
        # Should also test by feeding a df that is not a time series.
        with self.assertRaises(Exception):
            actual = baseflow.get_baseflow_chapman(nonsense, nonsense)
