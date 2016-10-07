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

"""
from pandas.util.testing import assert_frame_equal

class TestGetFunctions():

    def test_get_month(self):
        #"""
        #Test different month approach functions
        #"""
"""
        flowdata = pd.read_pickle("data/FlowData")
        temp = HydroAnalysis(flowdata)
        ms1 = temp.get_month("June").get_recess().data # full name
        ms2 = temp.get_month(6).get_recess().data # id
        assert_frame_equal(ms1, ms2)

        ms3 = temp.get_month("Jun").get_recess().data # abbr
        assert_frame_equal(ms1, ms3)
"""