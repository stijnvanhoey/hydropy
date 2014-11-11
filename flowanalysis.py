# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 18:14:28 2013

@author: VHOEYS
"""

import datetime

import numpy as np
import pandas as pd
from pandas.tseries.offsets import DateOffset

from reading_third_party_data import load_VMM_zrx_timeserie

#ALSO INCLUDE: Georgakakos2004 !!! ROC

class HydroAnalysis():
    '''
    The idea:
    handle the flow timeserie; definitions for splitting etc...

    first todo is some more thinking about how to set things up
    including ideas from hydromad, tiger,... and handling it flexible

    Attributes
    -----------
    data : pd.DataFrame
        time serie information with index the data-info and columns names
        the station identifiers
    data_cols :  list of str
        names of the columns containing data
    _hemisphere : 'north' or 'south'
        Providing info about the north or south hemisphere of the data
        series
    _season_type : astro or meteo
        The used definition of seasons, meteorological or astrological
    '''

    def __init__(self, data, dateformatstr="%d/%m/%Y", hemisphere="north",
                 season_type="meteo", datacols=None):
        """
        Time serie handling for the package centralized.

        Parameters
        -----------
        data : pd.DataFrame or convertable to pd.DataFrame
            a type that is convertable to a dataframe
        dateformatstr : str
            for non-default parsable datestrings e.g. "%d/%m/%Y"
        hemisphere : north | south
            data coming from north our southern hemisphere
        season_type : meteo | astro
            seasons started on meteorological of astrological time stamps
        datacols : None | list of str
            when None, all columns are interpreted as data column
        """
        if isinstance(data, pd.DataFrame):
            self.data = data
        else:
            try:
                self.data = pd.DataFrame(data)
            except:
                raise Exception("Input data not convertable to DataFrame.")

        #Control is necessary about the time-step-information.
        if not isinstance(self.data.index, pd.DatetimeIndex):
            try:

                self.data.index = pd.to_datetime(self.data.index,
                                                 format=dateformatstr)
            except:
                raise Exception("Date parsing not succeeded, \
                                        adapt dateformatstr-argument.")

        #Extract the meta-information (frequency,... and save it)
        if self.data.index.freq:
            self._frequency = self.data.index.freq
            #print "Frequency of the Time Serie is", self.data.index.freqstr
        else:
            guessed_freq = self.data.index.inferred_freq
            if guessed_freq:
                self.data.index = pd.DatetimeIndex(self.data.index,
                                                   freq=guessed_freq)
                self._frequency = guessed_freq
                #self.data = self.data.asfreq(guessed_freq) #needed?!?
                print "Frequency of the Time Serie is guessed as", \
                        self.data.index.freq
            else:
                print("Not able to interpret the time serie frequency,\
                      run the set_frequency to define the frequency!")

        # names of columns to use as data column for specific functions
        if datacols != None:
            #check fo existence
            for colname in datacols:
                if not colname in self.data.columns:
                    raise Exception(colname + " no current dataframe column name")
            self.data_cols = datacols
        else:
            self.data_cols = self.data.columns

        #Save start and enddate of the timeserie
        self._start_date = self.data.index[0]
        self._end_date = self.data.index[-1]

        #get all years of the timeserie
        self._years = range(self._start_date.year, self._end_date.year + 1)

        self._hemisphere = hemisphere
        self._season_type = season_type

        #Create selection masks
        self._mask_seasons()

    def __str__(self):
        return self.data.__repr__()

    def __repr__(self):
        message = 'Data columns '
        for name in self.data_cols:
            message += name + ', '
        message += 'ranging from ' + \
                        self._start_date.strftime("%H:%M:%S %d/%m/%Y") + \
                        ' till ' + \
                        self._end_date.strftime("%H:%M:%S %d/%m/%Y")
        message += ' with frequency ' + self.data.index.freqstr
        return message

    def __getitem__(self, val):
        """returns the class object itself with the selected values

        Provides also shortcut for date selection (pandas style):
        eg hydroobject["2009":"2011"] or
        """
        return self.__class__(self.data[val], datacols=self.data_cols)

    def _check_date_range(self, date2test):
        """controller for date range
        """
        if isinstance(date2test, str):
            date2test = pd.datetools.to_datetime(date2test)
        if not isinstance(date2test, datetime.datetime):
            raise Exception("Current str or datetime object \
                                                    could not be parsed.")
        if date2test < self._start_date or date2test > self._end_date:
            raise Exception("Provided date outside date range!")

    def frequency_change(self, freq="15T", *args, **kwargs):
        """
        Set the frequency of the time serie working with manually.

        Parameters
        -----------
        freq : str
            String with the frequency information. Typical examples are
            15min, H,...
        *args, **kwargs :
            Optionally provide fill method to pad/backfill missing values
            as extra arguments passed to pandas.asfreq function.

        See also:
        ---------
        http://pandas.pydata.org/pandas-docs/dev/timeseries.html#legacy-aliases
        """
        return self.__class__(self.data.asfreq(freq, *args, **kwargs),
                              datacols=self.data_cols)

    def frequency_resample(self, *args, **kwargs):
        """
        Link to the pandas esample function

        Examples
        ---------
        >>>  temp.frequency_resample('D', "mean") # Daily means
        """
        return self.__class__(self.data.resample(*args, **kwargs),
                              datacols=self.data_cols)

    def summary(self):
        """
        Returns summary/description of the data
        """
        return self.data.describe()

    def head(self, n=5):
        """
        """
        return self.data.head(n)

    def tail(self, n=5):
        """
        """
        return self.data.tail(n)

    def plot(self, *args, **kwargs):
        """quick pandas supported plot
        """
        return self.data.plot(*args, **kwargs)

    def current_date_range(self):
        """
        Returns summary/description of the data
        """
        print 'Time series from', self._start_date, 'till', self._end_date
        return self._start_date, self._end_date

    @classmethod
    def from_vmm_txt(cls, zrxfile):
        """
        Interprets the database outcome of a vmm file-type zrx-file
        """
        #todo
        vmm_serie = cls(load_VMM_zrx_timeserie(zrxfile))
        return vmm_serie

    @classmethod
    def from_txtdata_only(cls, filename, startdate,
                          enddate, freq,
                          header=None, dataname="Flow"):
        """
        Interprets the data of a 'dry' textfile and adds the date
        information to it

        Parameters
        ----------
        filename : str
            Full path and name of the file to read in
        startdate : string or datetime-like
            First timestamp of the time serie, eg "2005-12-31 23:00"
        enddate : string or datetime-like
            Last timestamp of the time serie, eg "2005-12-31 23:00"
        freq : string or DateOffset
            Frequency of the time serie
        header : int
            Number of lines to skip
        """
        date_index = pd.date_range(startdate, enddate, freq = freq)
        flowserie = pd.read_csv(filename, header = header)
        flowserie.index = date_index

        return cls(flowserie)

    @staticmethod
    def info_season_dates(hemisphere="north", definition_type="meteo"):
        """
        Get start date info for seasonal date selection.

        Parameters
        -----------
        hemisphere : 'north'|'south'
            Define the location of the weather station (north or south)
        definition_type : 'meteo'|'astro'
            Define the type of definition for the seasonal classification.
            Astronomical seasons are based on the position of the Earth in
            relation to the sun, whereas the meteorological seasons are based
            on the annual temperature cycle

        Returns
        --------
        Dictionary with the startvalues for each season (format: "mmdd")

        """
        if hemisphere == "north":
            if definition_type  == "meteo":
                return {"Summer" : "0601", "Autumn" : "0901",
                           "Winter": "1201", "Spring": "0301"}
            elif definition_type  == "astro":
                return {"Summer" : "0621", "Autumn" : "0921",
                           "Winter": "1221", "Spring": "0321"}
            else:
                raise Exception("Choose between meteo or \
                                    astro defined seasons.")
        elif hemisphere == "south":
            if definition_type  == "meteo":
                return {"Winter" : "0601", "Spring" : "0901",
                           "Summer": "1201", "Autumn": "0301"}
            elif definition_type  == "astro":
                return {"Winter" : "0621", "Spring" : "0921",
                           "Summer": "1221", "Autumn": "0321"}
            else:
                raise Exception("Choose between meteo or \
                                    astro defined seasons.")
        else:
            raise Exception("Choose between north and south hemisphere")

    def current_season_dates(self):
        """print info about current used season start dates
        """
        return self.info_season_dates(hemisphere=self._hemisphere,
                                     definition_type=self._season_type)

    @staticmethod
    def season_dates(season, year, seasondates):
        """str, str, dict -> (pd.Timestamp, pd.Timestamp)
        """
        season_startdate =  pd.Timestamp(year + seasondates[season])
        if season == "Winter":
            season_startdate = pd.Timestamp(str(int(year)-1) + \
                                                    seasondates[season])

        season_enddate = season_startdate + DateOffset(months = 3)
        #    print season + ": ", season_startdate, " till ", season_enddate
        return season_startdate, season_enddate

    @staticmethod
    def _exclude_nan(obs, mod):
        """pd.DataFrame, pd.DataFrame -> pd.DataFrame
        """
        obsmod =  pd.concat([obs, mod], axis = 1)
        obsmod.columns = ["obs","mod"]
        return obsmod.dropna()

    def get_date_range(self, start, end):
        """
        Link to pandas dataframe index date selection
        """
        self._check_date_range(start)
        self._check_date_range(end)
        return self.__class__(self.data[start : end],
                              datacols=self.data_cols)

    def get_year(self, year):
        """
        Select a subset of the timeserie by selecting all data of a specific
        year.

        Parameters
        -----------
        year : str
            Year to select data
        """
        if (not isinstance(year, str)) or len(year) != 4:
            raise TypeError("provide year in 4 character-string.")
        self._check_date_range(year)

        return self.__getitem__(year)

    def get_season(self, season):
        """
        If year is defined, only season of that year is selected,
        otherwise, all seasons from different years are pasted together.

        For winter, the year selected is from december of the previous year,
        till march of the selected year.
        """
        season = season.capitalize()
        #return self.__class__(self.data[self.data["season"] == season])
        df = self.data[self.data["season"] == season]
        df = df.asfreq(self.data.index.freq)
        return self.__class__(df, datacols=self.data_cols)

    def _mask_seasons(self):
        """
        Add column to data-sets with the season information
        """
        self.data["season"] = None
        seasons = self.current_season_dates()
        for year in self._years:
            for season in seasons.keys():
                season_start, \
                    season_end = self.season_dates(season, str(year),
                                                       seasons)
                self.data[season_start : season_end]["season"] = season

    def get_climbing(self):
        """
        """
        climbing = self.data[self.data_cols].diff() > 0.0
        df = self.data[climbing]
        df = df.asfreq(self.data.index.freq)
        return self.__class__(df, datacols=self.data_cols)

    def get_recess(self):
        """
        """
        recess = self.data[self.data_cols].diff() < 0.0
        df = self.data[recess]
        df = df.asfreq(self.data.index.freq)
        return self.__class__(df, datacols=self.data_cols)

#%%
    def get_modes(self):
        """
        Add column to data-sets providing information about:

            * driven
            * non-driven quick (above season-mean)
            * non-driven slow (below season-mean)
        """
        return True

    def get_highpeak_discharges(self):
        """
        Add column to data-sets with the season information
        """
        #use the peaks_above_percentile function

        return True

    def get_lowpeak_discharges(self):
        """
        Add column to data-sets with the season information
        """
        #use the peaks_below_percentile function
        return True

    def get_above_percentile(self):
        """
        Add column to data-sets with the season information
        """
        return True

    def get_below_percentile(self):
        """
        Add column to data-sets with the season information
        """
        return True

    def _mask_above_b04(self):
        """
        Add column to data-sets with the season information
        """
        return True

    def _mask_above_b08(self):
        """
        Add column to data-sets with the season information
        """
        return True

    def get_storms_per_year(self):
        """
        Add column to data-sets with the season information
        """
        #use selectstorms function
        return True

    def get_above_baseflow(self, baseflowdata):
        """
        Add column to data-sets with the season information
        """
        # use the baseflowdata
        return True

#    #The handling are static methods to make them useful on any pandas
#    #timeserie of dataframe object
#    @staticmethod  #useful when it doesn't use the itself!!
#    def summarize_it(df):
#        return df.describe()
#










