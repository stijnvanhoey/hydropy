# -*- coding: utf-8 -*-
"""
test_baseflow.py
@author: Martin Roberge
"""

from __future__ import absolute_import, print_function
import unittest

import numpy as np
import pandas as pd

import hydropy as hp

time = pd.date_range('1/1/2010', periods=100, freq='D')
discharge = pd.DataFrame(np.random.randn(len(time)), index=time, columns=['Qtest'])


class TestBaseflow(unittest.TestCase):

    def test_baseflow_get_bf_chapman_returns_dataframe(self):
        actual = hp.get_baseflow_chapman(discharge, 0.0001)
        self.assertIs(type(actual), pd.DataFrame)

    def test_baseflow_get_bf_boughton_returns_dataframe(self):
        actual = hp.get_baseflow_boughton(discharge, 0.5, 0.0001)
        self.assertIs(type(actual), pd.DataFrame)

    def test_baseflow_get_bf_ihacres_returns_dataframe(self):
        actual = hp.get_baseflow_ihacres(discharge, 0.5, 0.5, 0.0001)
        self.assertIs(type(actual), pd.DataFrame)
