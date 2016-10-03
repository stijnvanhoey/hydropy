# -*- coding: utf-8 -*-
"""
test_flowanalysis.py
"""

from __future__ import absolute_import, print_function
import unittest

from hydropy import flowanalysis as fa


class TestHydroAnalysis(unittest.TestCase):

    def test_HydroAnalysis_raises_exception_when_fed_bad_data(self):
        nonsense = "meaningless data"
        # Note: it might make more sense to make this raise a TypeError
        with self.assertRaises(Exception):
            actual = fa.HydroAnalysis(nonsense)
