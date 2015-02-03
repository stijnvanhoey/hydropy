# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 12:04:27 2014

@author: stvhoey
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from hydropy import HydroAnalysis


flowdata = pd.read_pickle("../data/FlowData")
raindata = pd.read_pickle("../data/RainData")
flow2use = flowdata["L06_347"]

temp = HydroAnalysis(flowdata)#, datacols=['LS06_342'])
tempshort = temp.get_year("2011")


#TODO!!!!! make return self ipv die return eigen obect voor geheugenstuff!
#TODO: ignore NAN


test = tempshort.get_highpeaks(350)

#test = tempshort.get_lowpeaks(50, below_percentile=1.)
fig, ax = plt.subplots()
test["LS06_34C"].plot(ax=ax, style = 'o')
tempshort["LS06_34C"].plot(ax=ax)

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
