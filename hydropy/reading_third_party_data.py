# -*- coding: utf-8 -*-
"""
Reading data files from external sources

Stijn Van Hoey, stvhoey.vanhoey@ugent.be
"""
from __future__ import absolute_import, print_function

import os
import sys

import ftplib
from io import StringIO
import datetime

import pandas as pd


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

    #define header length (= number of lines with starting #)
    ctestall = zrxf
    headerlength = 0
    ctest = '#'
    while ctest == '#':
        ctest = ctestall.readline()[0]
        headerlength += 1
    print('File ', filename.split("\\")[-1],\
            ' headerlength is: ', headerlength-1)
    zrxf.close()

    #Read the data
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
    ftp.retrlines("RETR " + filename, lambda s, w = outfile.write: w(s+"\n"))


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
    #discharge -> go to discharge folder
    ftp.cwd(path)
    #check the files in the folder
    files = ftp.nlst()

    # We're interested in the .zrx files, so let's get the information of
    # those in a dictionary, with the key the station code and the data a
    # pandas Dataframe first exclude in the files list the none-zrx files
    files = [zrxf for zrxf in files if '.zrx' in zrxf]

    data = []
    for zrxf in files:
        output = StringIO.StringIO()
        _gettext(ftp, zrxf, output)

        #define header length (= number of lines with starting #)
        ctestall = StringIO.StringIO(output.getvalue())
        headerlength = 0
        ctest = '#'
        while ctest == '#':
            ctest = ctestall.readline()[0]
            headerlength += 1
        print('File ',zrxf,' headerlength is: ', headerlength-1)

        temp = pd.read_table(StringIO.StringIO(output.getvalue()), sep=' ',
                           skiprows=headerlength-1, index_col=0,
                           parse_dates=True,
                           header=None, usecols=(0, 1),
                           names=['Time', zrxf[:-4]], na_values='-777.0')
        data.append(temp)
        output.close()
    ftp.close()

    ##CONCATENATE THE DIFFERENT DATAFRAMES IN ONE BIG:
    data2 = pd.concat(data, axis=1)

    ##SAVE THE DATA IN ONE PICKLE FOR NEXT TIME WORKING WITH THESE
    data2.to_csv(datetime.datetime.now().strftime("%Y%m%d") +
                    "VMM_" + dataname+".csv", float_format="%.3f",
                    na_rep="Nan")
    data2.to_pickle(datetime.datetime.now().strftime("%Y%m%d")
                    + "VMM_" + dataname)


def _minutes2hours(minutes):
    """convert minutes to hours and return als rest
    """
    return minutes/60, minutes%60


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
    parse = lambda y,m,d,h: datetime.datetime(int(y), int(m), int(d),
                                              _minutes2hours(int(h))[0],
                                              _minutes2hours(int(h))[1])
    ceh_data = pd.read_csv(filename, sep=',',
                       parse_dates={"Datetime":[1,2,3,4]},
                       date_parser=parse,
                       skipinitialspace=True)
    ceh_data = ceh_data.set_index("Datetime")

    return ceh_data
