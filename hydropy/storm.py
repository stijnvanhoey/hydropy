# -*- coding: utf-8 -*-
"""
Hydropy package

@author: Stijn Van Hoey
"""

import datetime

import numpy as np
import pandas as pd
from pandas.tseries.offsets import DateOffset, Day, Week, Hour, Minute

def selectstorms(flowserie, rainserie, number_of_storms = 3, drywindow = 96):
    """ (pd.DataFrame, pd.DataFrame) -> List
    Easy storm selection process, based on the maximum flows measured
    in the given timeserie of flow measurements.

    To define the startdate of the storm, 24h no rain before the Qmax is
    searched for. The end date is found by checking the
    flow at the startdate (Qbase) and searching the moment after Qmax with
    the same flow. If none is found, relaxation (1.1*Qbase; 1.2*Qbase,...)
    until a moment is found.

    Parameters
    ----------
    flowserie : pd.Series
        Pandas Series with the date in the index
    rainserie : pd.Series
        Pandas Series with the date in the index

    """
    if not isinstance(flowserie, pd.Series):
        raise Exception('flowserie is a single data Series')
    if not isinstance(rainserie, pd.Series):
        raise Exception('rainserie is a single data Series')

    #fill na values with very low (negative) value
    temp = flowserie.fillna(value=-777.).copy()
    #sort the whole array
    try:
        temp = temp.sort(temp.columns.tolist(), ascending=False)
    except:
        temp.sort(ascending=False)

    #find in the index three periods which are at least a week from each other
    #after three concurrences, save these dates
    stormmax = [temp.index[0]] #first element is a selected storm
    i = 1
    while len(stormmax) < number_of_storms:
        #check for each period
        alldif = True
        for stormdate in stormmax:
            if abs(temp.index[i] - stormdate) < datetime.timedelta(days=7):
                alldif = False
        #if new stormperiod, select
        if alldif:
            stormmax.append(temp.index[i])
        i+=1

    selstorms = []
    for storm in stormmax:
        ##FIND DRY DAY WEEK BEFORE
        #select period before storm (1 week)
        temp1 = rainserie[storm - Week():storm]
        temp1 = pd.rolling_sum(temp1, window = drywindow, center = False)
        #zero value means the preceding 24hours no rain: so, closest zeros
        #to the date itself -24h are selected
        if rainserie.ndim == 2:
            temp1 = temp1.min(axis=1)
        tempdates = temp1[temp1 < 0.001].index.tolist()
        if len(tempdates) == 0:
            raise Exception('Extend drywindow period before stormpoint.')

        date_arg = np.argmin([abs(times - storm) for times in tempdates])
        startstormdate = tempdates[date_arg] - Day()

        #Get the flow value of the storm and when it is found again + 1 Day
        temp2a = flowserie[startstormdate:startstormdate + Week()*2]

        #only if multiple columns
        if flowserie.ndim == 2:
            temp2 = temp2a.max(axis=1)
        else:
            temp2 = temp2a

        flowbase = temp2.ix[startstormdate]
        lowerafterstorm = temp2[temp2 < flowbase][storm + Day():]
        if lowerafterstorm.size == 0:
            print 'Lower initial flow not found again...test with mean...'
            if flowserie.ndim == 2:
                temp2 = temp2a.mean(axis=1)
            else:
                temp2 = temp2a
            flowbase = temp2.ix[startstormdate]
            lowerafterstorm = temp2[temp2 < flowbase][storm + Day():]
        cnt = 1
        while lowerafterstorm.size == 0:
            print '...    still not working; relaxing conditions...', \
                cnt*10, '% of minimal after storm incorporated'
            flowbase = flowbase + 0.1*flowbase
            lowerafterstorm = temp2[temp2 < flowbase][storm + Day():]
            cnt += 1
        endstormdate = lowerafterstorm.index[0]

        #add to selected storms
        selstorms.append({'startdate':startstormdate,'enddate':endstormdate})

    return selstorms