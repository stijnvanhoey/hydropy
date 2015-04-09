# -*- coding: utf-8 -*-
"""
Hydropy package

@author: Stijn Van Hoey
"""

import numpy as np
import pandas as pd
import seaborn as sns
sns.set_style('whitegrid')
import matplotlib.pyplot as plt

from hydropy import HydroAnalysis
from storm import selectstorms

flowdata = pd.read_pickle("../data/FlowData")
raindata = pd.read_pickle("../data/RainData")
flow2use = flowdata["L06_347"]

myflowserie = HydroAnalysis(flowdata)#, datacols=['LS06_342'])
myflowserie_short = myflowserie['LS06_347'].get_year("2010")

#%%

# Select the summer of 2009:
myflowserie.get_year('2009').get_season("Summer").plot(figsize=(12,6))

#%% Select all June data
flow_june = myflowserie.get_month("Jun")
flow_june_df = flow_june.get_data_only()

#%%  recession in June 2010
myflowserie.get_year('2011').get_month("Jun").get_recess().plot(figsize=(12,6))

#%%
fig, ax = plt.subplots(figsize=(13, 6))
myflowserie['LS06_347'].get_year('2010').get_month("Jul").get_highpeaks(150, above_percentile=0.9).plot(style='o', ax=ax)
myflowserie['LS06_347'].get_year('2010').get_month("Jul").plot(ax=ax)

#%%
fig, ax = plt.subplots(figsize=(13, 6))
myflowserie['LS06_347'].get_year('2010').get_month("Jul").get_lowpeaks(50, below_percentile=1.).plot(style='o', ax=ax)
myflowserie['LS06_347'].get_year('2010').get_month("Jul").plot(ax=ax)

#%%
selectstorms(flowdata['LS06_347'], raindata['P05_039'], number_of_storms = 3, drywindow = 96)



#%% READY MADE FOR UNIT TEST PURPOSES
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
