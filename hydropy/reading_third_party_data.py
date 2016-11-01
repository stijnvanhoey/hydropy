# -*- coding: utf-8 -*-
"""
Reading data from external sources

Stijn Van Hoey, stvhoey.vanhoey@ugent.be
Martin Roberge, mroberge@towson.edu
"""
from __future__ import absolute_import, print_function

import os
import sys
import ftplib
from io import StringIO
import datetime

import numpy as np
import pandas as pd
import requests

from . import exceptions


def load_VMM_zrx_timeserie(filename):
    """
    Read VMM zrx files and converts it into a pd.DataFrame

    Parameters
    ----------
    filename : str
        full path name to the file to read in

    Returns
    -------
    data : pd.DataFrame
        pd.DataFrame of the VMM data
    """
    zrxf = open(filename, 'r')

    # define header length (= number of lines with starting #)
    ctestall = zrxf
    headerlength = 0
    ctest = '#'
    while ctest == '#':
        ctest = ctestall.readline()[0]
        headerlength += 1
    print('File ', filename.split("\\")[-1],
          ' headerlength is: ', headerlength-1)
    zrxf.close()

    # Read the data
    data = pd.read_table(filename, sep=' ',
                         skiprows=headerlength-1, index_col=0,
                         parse_dates=True,
                         header=None, usecols=(0, 1),
                         names=['Time', filename.split("\\")[-1][:-4]],
                         na_values='-777.0')
    return data


def _gettext(ftp, filename, outfile=None):
    """
    Help function for scraping text from the ftp-driver
    (for binary data, another format would be needed)

    """
    # fetch a text file
    if outfile is None:
        outfile = sys.stdout
    # use a lambda to add newlines to the lines read from the server
    ftp.retrlines("RETR " + filename, lambda s, w=outfile.write: w(s+"\n"))


def load_VMM_zrx_timeseries_from_ftp(server, login, password,
                                     path, dataname="_DATA"):
    """
    Read all VMM zrx files in a specific folder, concatenates them
    and converts it into a pd.DataFrame

    Parameters
    ----------
    server : str
        ftp server location, e.g. ftp.anteagroup.be
    login : str
        login name of the ftp drive
    password : str
        password of the user
    path : str
        path name to the folder with the interested .zrx files
    dataname : str
        suffix name used to flag the saved data

    Returns
    -------
    data : pd.DataFrame
        pd.DataFrame of the VMM data
    """
    ftp = ftplib.FTP(server)
    ftp.login(login, password)
    # discharge -> go to discharge folder
    ftp.cwd(path)
    # check the files in the folder
    files = ftp.nlst()

    # We're interested in the .zrx files, so let's get the information of
    # those in a dictionary, with the key the station code and the data a
    # pandas Dataframe first exclude in the files list the none-zrx files
    files = [zrxf for zrxf in files if '.zrx' in zrxf]

    data = []
    for zrxf in files:
        output = StringIO.StringIO()
        _gettext(ftp, zrxf, output)

        # define header length (= number of lines with starting #)
        ctestall = StringIO.StringIO(output.getvalue())
        headerlength = 0
        ctest = '#'
        while ctest == '#':
            ctest = ctestall.readline()[0]
            headerlength += 1
        print('File ', zrxf, ' headerlength is: ', headerlength-1)

        temp = pd.read_table(StringIO.StringIO(output.getvalue()), sep=' ',
                             skiprows=headerlength-1, index_col=0,
                             parse_dates=True,
                             header=None, usecols=(0, 1),
                             names=['Time', zrxf[:-4]], na_values='-777.0')
        data.append(temp)
        output.close()
    ftp.close()

    # CONCATENATE THE DIFFERENT DATAFRAMES IN ONE BIG:
    data2 = pd.concat(data, axis=1)

    # SAVE THE DATA IN ONE PICKLE FOR NEXT TIME WORKING WITH THESE
    data2.to_csv(datetime.datetime.now().strftime("%Y%m%d") +
                 "VMM_" + dataname+".csv", float_format="%.3f",
                 na_rep="Nan")
    data2.to_pickle(datetime.datetime.now().strftime("%Y%m%d") +
                    "VMM_" + dataname)


def _minutes2hours(minutes):
    """convert minutes to hours and return als rest
    """
    return minutes/60, minutes % 60


def load_CEH_timeserie(filename):
    """
    Read VMM zrx files and converts it into a pd.DataFrame

    Parameters
    ----------
    filename : str
        full path name to the file to read in

    Returns
    -------
    data : pd.DataFrame
        pd.DataFrame of the VMM data
    """
    parse = lambda y, m, d, h: datetime.datetime(int(y), int(m), int(d),
                                                 _minutes2hours(int(h))[0],
                                                 _minutes2hours(int(h))[1])
    ceh_data = pd.read_csv(filename, sep=',',
                           parse_dates={"Datetime": [1, 2, 3, 4]},
                           date_parser=parse,
                           skipinitialspace=True)
    ceh_data = ceh_data.set_index("Datetime")

    return ceh_data


def get_usgs(site, service, start_date, end_date):
    """Request stream gauge data from the USGS NWIS.

    Args:
        site (str):
            a valid site is 01585200
        service (str):
            can either be 'iv' or 'dv' for instantaneous or daily data.
            iv data are instantaneous values usually recorded every 15 minutes;
                units are expressed as cubic feet/second.
            dv data are daily mean discharges expressed as cubic feet/second.
        start_date (str):
           should take on the form yyyy-mm-dd
        end_date (str):
            should take on the form yyyy-mm-dd

    Returns:
        A Pandas dataframe object.

    Raises:
        ConnectionError  due to connection problems like refused connection
            or DNS Error.
        HydroNoDataError  when the request is valid, but NWIS has no data for
            the parameters provided in the request.

    Example::

        >>> from hydropy import hydropy as hp
        >>> my_df = hp.get_usgs('01585200', 'dv', '2012-06-01', '2012-06-05')

        >>> my_df
                    value
        datetime
        2012-06-01  97.00
        2012-06-02   5.80
        2012-06-03   1.70
        2012-06-04   1.40
        2012-06-05   0.96
    """
    response_obj = request_nwis(site, service, start_date, end_date)
    nwis_df = extract_nwis_df(response_obj)

    return nwis_df


def request_nwis(site, service, start_date, end_date):
    """Request stream gauge data from the USGS NWIS.

    Args:
        site (str):
            a valid site is 01585200
        service (str):
            can either be 'iv' or 'dv' for instantaneous or daily data.
        start_date (str):
           should take on the form yyyy-mm-dd
        end_date (str):
            should take on the form yyyy-mm-dd

    Returns:
        a response object.

            * response.url: the url we requested data from.
            * response.status_code:
            * response.json: the content translated as json
            * response.ok: "True" when we get a '200'

    Raises:
        ConnectionError  due to connection problems like refused connection
            or DNS Error.

    Example::

        >>> import hydropy as hp
        >>> # this requests: http://waterservices.usgs.gov/nwis/dv/?format=json,1.1&sites=01585200&startDT=2012-06-01&endDT=2012-06-05
        >>> response = hp.get_nwis('01585200', 'dv', '2012-06-01', '2012-06-05')


        >>> response
        <response [200]>
        >>> response.ok
        True
        >>> response.json()
        *JSON ensues*

    The specification for this service is located here:
    http://waterservices.usgs.gov/rest/IV-Service.html
    """

    header = {
        'Accept-encoding': 'gzip',
        'max-age': '120'
        }

    values = {
        'format': 'json,1.1',
        'sites': site,
        'parameterCd': '00060',  # represents stream discharge.
        # 'period': 'P10D' # This is the format for requesting data for a
        # number of days before today. If no start or end date are supplied,
        # NWIS will default to period = 1 and return the most recent day of
        # data.
        'startDT': start_date,
        'endDT': end_date
        }

    url = 'http://waterservices.usgs.gov/nwis/'
    url = url + service + '/?'
    response = requests.get(url, params=values, headers=header)
    # requests will raise a 'ConnectionError' if the connection is refused
    # or if we are disconnected from the internet.
    # I think that is appropriate, so I don't want to handle this error.

    # TODO: where should all unhelpful ('404' etc) responses be handled?
    return response


def extract_nwis_df(response_obj):
    """Returns a Pandas dataframe from an NWIS response object.

    Returns:
        a pandas dataframe.

    Raises:
        HydroNoDataError  when the request is valid, but NWIS has no data for
            the parameters provided in the request.
    """
    nwis_dict = response_obj.json()

    # strip header and all metadata.
    ts = nwis_dict['value']['timeSeries']
    if ts == []:
        # raise a HydroNoDataError if NWIS returns an empty set.
        #
        # Ideally, an empty set exception would be raised when the request
        # is first returned, but I do it here so that the data doesn't get
        # extracted twice.
        # TODO: raise this exception earlier??
        #
        # ** Interactive sessions should have an error raised.
        #
        # **Automated systems should catch these errors and deal with them.
        # In this case, if NWIS returns an empty set, then the request
        # needs to be reconsidered. The request was valid somehow, but
        # there is no data being collected.

        # TODO: this if clause needs to be tested.
        raise exceptions.HydroNoDataError("The NWIS reports that it does not"
                                          " have any data for this request.")

    data = nwis_dict['value']['timeSeries'][0]['values'][0]['value']
    # print("inside extract_nwis_df")
    # print(data)
    DF = pd.DataFrame(data, columns=['dateTime', 'value'])
    DF.index = pd.to_datetime(DF.pop('dateTime'))
    DF.value = DF.value.astype(float)
    # DF.index.name = None
    DF.index.name = 'datetime'
    # this is never tested
    DF.replace(to_replace='-999999', value=np.nan, inplace=True)

    return DF
