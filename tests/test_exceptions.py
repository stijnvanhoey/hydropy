# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 21:46:47 2016

@author: Marty
"""
from __future__ import absolute_import
import unittest

from hydropy import exceptions

class TestExceptions(unittest.TestCase):

    def test_exceptions_HydroNoDataError_can_be_raised(self):
        with self.assertRaises(exceptions.HydroNoDataError):
            raise exceptions.HydroNoDataError("Test Error!!")
