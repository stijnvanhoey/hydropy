# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 15:46:38 2016

@author: mroberge
"""
from __future__ import absolute_import, print_function
import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import pandas as pd

import hydropy
from hydropy import hdf5 as hp


class TestHD5(unittest.TestCase):

    def test_hdf5_saves_file(self):
        pass
