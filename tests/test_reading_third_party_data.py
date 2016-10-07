# -*- coding: utf-8 -*-
"""
test_reading_third_party_data.py
"""

from __future__ import absolute_import, print_function
import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import pandas as pd

from hydropy import reading_third_party_data as r3p
from hydropy import exceptions

good_json = {'declaredType': 'org.cuahsi.waterml.TimeSeriesResponseType',
 'globalScope': True,
 'name': 'ns1:timeSeriesResponseType',
 'nil': False,
 'scope': 'javax.xml.bind.JAXBElement$GlobalScope',
 'typeSubstituted': False,
 'value': {'queryInfo': {'criteria': {'locationParam': '[ALL:01589440]',
    'parameter': [],
    'timeParam': {'beginDateTime': '2013-01-01T00:00:00.000',
     'endDateTime': '2013-01-05T00:00:00.000'},
    'variableParam': '[00060]'},
   'note': [{'title': 'filter:sites', 'value': '[ALL:01589440]'},
    {'title': 'filter:timeRange',
     'value': '[mode=RANGE, modifiedSince=null] interval={INTERVAL[2013-01-01T00:00:00.000-05:00/2013-01-05T00:00:00.000-05:00]}'},
    {'title': 'filter:methodId', 'value': 'methodIds=[ALL]'},
    {'title': 'requestDT', 'value': '2016-10-05T03:08:13.704Z'},
    {'title': 'requestId', 'value': 'f42bd170-8aa8-11e6-b36a-6cae8b663fb6'},
    {'title': 'disclaimer',
     'value': 'Provisional data are subject to revision. Go to http://waterdata.usgs.gov/nwis/help/?provisional for more information.'},
    {'title': 'server', 'value': 'vaas01'}],
   'queryURL': 'http://waterservices.usgs.gov/nwis/dv/startDT=2013-01-01&sites=01589440&format=json%2C1.1&parameterCd=00060&endDT=2013-01-05'},
  'timeSeries': [{'name': 'USGS:01589440:00060:00003',
    'sourceInfo': {'geoLocation': {'geogLocation': {'latitude': 39.3917222,
       'longitude': -76.6609444,
       'srs': 'EPSG:4326'},
      'localSiteXY': []},
     'note': [],
     'siteCode': [{'agencyCode': 'USGS',
       'network': 'NWIS',
       'value': '01589440'}],
     'siteName': 'JONES FALLS AT SORRENTO, MD',
     'siteProperty': [{'name': 'siteTypeCd', 'value': 'ST'},
      {'name': 'hucCd', 'value': '02060003'},
      {'name': 'stateCd', 'value': '24'},
      {'name': 'countyCd', 'value': '24005'}],
     'siteType': [],
     'timeZoneInfo': {'daylightSavingsTimeZone': {'zoneAbbreviation': 'EDT',
       'zoneOffset': '-04:00'},
      'defaultTimeZone': {'zoneAbbreviation': 'EST', 'zoneOffset': '-05:00'},
      'siteUsesDaylightSavingsTime': False}},
    'values': [{'censorCode': [],
      'method': [{'methodDescription': '', 'methodID': 68299}],
      'offset': [],
      'qualifier': [{'network': 'NWIS',
        'qualifierCode': 'A',
        'qualifierDescription': 'Approved for publication -- Processing and review completed.',
        'qualifierID': 0,
        'vocabulary': 'uv_rmk_cd'}],
      'qualityControlLevel': [],
      'sample': [],
      'source': [],
      'value': [{'dateTime': '2013-01-01T00:00:00.000',
        'qualifiers': ['A'],
        'value': '29'},
       {'dateTime': '2013-01-02T00:00:00.000',
        'qualifiers': ['A'],
        'value': '27'},
       {'dateTime': '2013-01-03T00:00:00.000',
        'qualifiers': ['A'],
        'value': '25'},
       {'dateTime': '2013-01-04T00:00:00.000',
        'qualifiers': ['A'],
        'value': '25'},
       {'dateTime': '2013-01-05T00:00:00.000',
        'qualifiers': ['A'],
        'value': '24'}]}],
    'variable': {'noDataValue': -999999.0,
     'note': [],
     'oid': '45807197',
     'options': {'option': [{'name': 'Statistic',
        'optionCode': '00003',
        'value': 'Mean'}]},
     'unit': {'unitCode': 'ft3/s'},
     'valueType': 'Derived Value',
     'variableCode': [{'default': True,
       'network': 'NWIS',
       'value': '00060',
       'variableID': 45807197,
       'vocabulary': 'NWIS:UnitValues'}],
     'variableDescription': 'Discharge, cubic feet per second',
     'variableName': 'Streamflow, ft&#179;/s',
     'variableProperty': []}}]}}

class TestReadVMM(unittest.TestCase):

    def test_r3p_load_VMM_zrx_timeserie_returns_df(self):
        pass


class TestGetUSGS(unittest.TestCase):
    """
        Situation --> Expected result
        user enters bad parameters --> an exception that explains the proper format.
        user enters a start that is before end date --> ???
        user enters a site that doesn't exist --> [] returned, HydroNoDataError
        user enters dates with no data --> [] returned, HydroNoDataError
        Weird Status Code returned --> Show it to the user

        What conditions do I need to test get_usgs for?
        Is an exception raised for bad inputs before request.get called?
        Does request.get get called with correct parameters?
        Does the returned response get handled properly?
            response.ok == false  ...now what?
        Does extract_nwis_df warn when there is no data?
        Does extract_nwis_df extract a nicely formed df?
    """

    @mock.patch('requests.get')
    def test_r3p_request_nwis_calls_with_expected_params(self, mock_get):
        """
        Thanks to
        http://engineroom.trackmaven.com/blog/making-a-mockery-of-python/
        """

        site = 'A'
        service = 'B'
        start = 'C'
        end = 'D'

        expected_url = 'http://waterservices.usgs.gov/nwis/B/?'
        expected_headers = {'max-age': '120', 'Accept-encoding': 'gzip'}
        expected_params = {'format': 'json,1.1', 'sites': 'A', 'endDT': 'D',
                           'startDT': 'C', 'parameterCd': '00060'}
        expected = 'mock data'

        mock_get.return_value = expected
        actual = r3p.request_nwis(site, service, start, end)
        mock_get.assert_called_once_with(expected_url, params=expected_params,
                                         headers=expected_headers)
        self.assertEqual(actual, expected)


    def test_r3p_extract_nwis_df_raises_HydroNoDataError(self):
        """Call extract_nwis_df with a fake object.
        Normally, it is expecting a Requests response object with a
        functioning .json() method. Surprise! Instead we send a fake response,
        with a .json() method that returns NWIS json with no data.
        Will this raise an error?  Let's find out:
        """
        # alternative 1: class Fake(object): json = lambda: []
        # alternative 2: make a new response object from the requests lib.
        class FakeResponse(object):
            def json():
                my_json = {'value': {'timeSeries': []}}
                return my_json

        fake_response = FakeResponse

        with self.assertRaises(exceptions.HydroNoDataError):
            r3p.extract_nwis_df(fake_response)


    def test_r3p_extract_nwis_df(self):
        # Does it really make sense to define a class inside of a test function
        class FakeResponse(object):
            def json():
                return good_json

        fake_response = FakeResponse

        actual = r3p.extract_nwis_df(fake_response)
        self.assertIs(type(actual), pd.core.frame.DataFrame,
                      msg="Did not return a df")

    @unittest.skip("Need to test whether missing values replaced with NaN")
    def test_r3p_extract_nwis_df_replaces_novalues_NaN(self):
        fail
        
        
    @unittest.skip("Need more tests for get_usgs")
    def test_r3p_get_usgs(self):
        self.assertTrue(False)
