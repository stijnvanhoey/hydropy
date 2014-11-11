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

#example of concatenated selection of the time series:
subset1 = temp.get_season("summer").get_year("2010").get_recess()

#! test for both single column as multicolumn
