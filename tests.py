# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 12:04:27 2014

@author: stvhoey
"""

import numpy as np
import pandas as pd

from baseflow import *
from flowanalysis import HydroAnalysis

flowdata = pd.read_pickle("FlowData")
raindata = pd.read_pickle("RainData")
flow2use = flowdata["L06_347"]

temp = HydroAnalysis(flowdata)#, datacols=['LS06_342'])
tempshort = temp.get_year("2011")
tempshort.get_highpeaks(150)

#example of concatenated selection of the time series:
#subset1 = temp.get_season("summer").get_year("2010").get_recess()

#! test for both single column as multicolumn ok
#tt = temp["L06_347"].get_year("2010").get_month("Jun")






# READY MADE FOR UNIT TEST PURPOSES
from pandas.util.testing import assert_frame_equal

class TestGetFunctions():

    def test_get_month(self):
        """
        Test different month approach functions
        """
        ms1 = temp.get_month("June").get_recess().data # full name
        ms2 = temp.get_month(6).get_recess().data # id
        assert_frame_equal(ms1, ms2)

        ms3 = temp.get_month("Jun").get_recess().data # abbr
        assert_frame_equal(ms1, ms3)





