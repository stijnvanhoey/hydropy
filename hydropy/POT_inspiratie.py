#-------------------------------------------------------------------------------
# Name:        Extracting nearly independent peak and low flows AND OTHERS
# Purpose:     P. Willems, EnvironModel&Softw 24 (2009), 311-321
#
# Author:      VHOEYS
#
# Created:     24/05/2011
# Copyright:   (c) VHOEYS 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

#Import general packages
import sys
import numpy as np
import numpy.ma as ma
import random as rd
import scikits.timeseries as ts

import calendar
#import matplotlib.pyplot as plt
#import scikits.timeseries.lib.plotlib as tpl
#import scikits.timeseries.lib.reportlib as rl

#Import framework packages
#from FDC import *               #SVH-package
#from CRVC import *              #SVH-package
#from plot_functies import *     #SVH-package
#from obj_functies import *	    #SVH-package

def getDriven(FlowIn,RainIn,laghours=24):
    '''
    driven by rain
    '''
    driven=ma.masked_where(RainIn < 0.001 ,FlowIn)
    #TODO: LAGHOURS MOMENTEN TOEVOEGEN
#    print 'lag-hours not yet implemented'
    return driven,np.array(driven.mask.copy())

def getnonDrivenQuick(FlowIn,rain1,FMean,laghours=24):
    '''
    Driven by rainfall , based on slope + higher than mean

    ! NEED WINTER/SUMMER BASED, otherwise stupid results: FMEAN
    need timeserie object
    '''

    nondriven=ma.masked_where(rain1 > 0.001 ,FlowIn)
    #all values higher than mean value of season
    FlowAbove=ma.masked_where(nondriven-FMean < 0.0,nondriven)
    FlowAbove.unshare_mask()
    return getRecess(FlowAbove)


def getnonDrivenSlow(FlowIn,rain1,FMean,laghours=24):
    '''
    Driven by rainfall , based on slope + higher than mean

    ! NEED WINTER/SUMMER BASED, otherwise stupid results

    need timeserie object
    '''
    nondriven=ma.masked_where(rain1 > 0.001 ,FlowIn)

    #all values higher than mean value of season
    FlowUnder=ma.masked_where(nondriven-FMean > 0.0,nondriven)
    FlowUnder.unshare_mask()
    return getRecess(FlowUnder)


def peakdet(v, delta, x = None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html

    Currently returns two lists of tuples, but maybe arrays would be better

    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.

    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.

    """
    maxtab = []
    mintab = []

    if x is None:
        x = np.arange(len(v))

    loc = np.arange(len(v))
    v = np.asarray(v)

    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')

    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')

    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = np.Inf, -np.Inf
    mnpos, mxpos = np.NaN, np.NaN

    lookformax = True

    for i in np.arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return maxtab, mintab

def dry_wet_spells(ts, threshold):
 """
 returns the duration of spells below and above threshold

 input
 -----
 ts          a pandas timeseries
 threshold   threshold below and above which dates are counted

 output
 ------
 ntot_ts               total number of measurements in ts
 n_lt_threshold        number of measurements below threshold
 storage_n_cons_days   array that stores the lengths of sequences
                       storage_n_cons_days[0] for dry days
                       storage_n_cons_days[1] for wet days
 """
 # total number in ts
 ntot_ts = ts[~ ts.isnull()].count()
 # number lt threshold
 n_lt_threshold = ts[ts <= threshold].count()

 # type_day = 0   # dry
 # type_day = 1   # wet

 # initialisierung: was ist der erste Tag
 type_prev_day = 0
 storage_n_cons_days = [[],[]]
 n_cons_days = 0

 for cur_day in ts[~ ts.isnull()]:
     # current day is dry
     if cur_day <= threshold:
         type_cur_day = 0
         if type_cur_day == type_prev_day:
             n_cons_days += 1
         else:
             storage_n_cons_days[1].append(n_cons_days)
             n_cons_days = 1
         type_prev_day = type_cur_day
     else:
         type_cur_day = 1
         if type_cur_day == type_prev_day:
             n_cons_days += 1
         else:
             storage_n_cons_days[0].append(n_cons_days)
             n_cons_days = 1
         type_prev_day = type_cur_day

 return ntot_ts, n_lt_threshold, storage_n_cons_days

# ntot_ts, n_lt_threshold, storage_n_cons_days = dry_wet_spells(raindata['P05_039'], 0.2)

###########################################################################
###IMPORT DATA                                                           ##
###########################################################################
#
### REAL DATA NETE 1998-2008### ( Beter te doen met ts.timeseries zoals in framework)
##Lezen Discharge data
#dateconverter = lambda d,h: ts.Date('H', day=int(str(d)[8:10]), month=int(str(d)[5:7]), year=int(str(d)[0:4]),hour=int(str(h)[0:2]))
#Flow=ts.tsfromtxt('Data\discharge_geel-zammel.txt',skip_header=3,datecols=(0,1),dateconverter=dateconverter,freq='H',asrecarray=True,missing_values='NaN')
#
##Lezen subflows from filter
#dateconverter = lambda d,h: ts.Date('H', day=int(str(d)[0:2]), month=int(str(d)[3:5]), year=int(str(d)[6:10]),hour=int(str(h)[0:2]))
#FilterBase=ts.tsfromtxt('Data\Filter_Baseflow3.txt',skip_header=1,datecols=(0,1),dateconverter=dateconverter,freq='H',asrecarray=True,missing_values='NaN')
#
##Extract Calibration Period
#start_date = ts.Date(freq='H', year=2002, month=8, day=12,hour=9)
#end_date = ts.Date(freq='H', year=2005, month=12, day=31,hour=23)
#
#FlowCalib=ts.TimeSeries.adjust_endpoints(Flow.f2, start_date, end_date)
#FilterBaseCalib=ts.TimeSeries.adjust_endpoints(FilterBase.f2, start_date, end_date)
###CalibData=TS_SameScaleVHM(FlowCalib,FilterBaseCalib,label1=r'River Flow Series',label2=r'Baseflow filter result',xlabelt=r'Date',ylabelt=r'Q $(m^3/s)$',titlet=r' ',saveit=False)
###CalibData.savefig('Flow&base.png', dpi=300, facecolor='w', edgecolor='w',orientation='portrait', papertype=None,transparent=False)
#
#FL=FlowCalib.data
#
#t=np.arange(0.0,10.0,0.1)
#x=sin(2*t) - 3*cos(3.8*t)
#
##PARS for POT analysis
#kp=10 #timesteps
#f=0.5
#q_lim=2  #m3/s
#
#pks=peakdet(FL, 0.01, x = FlowCalib.dates)
#plt.figure()
#plt.grid()
#plt.plot(FlowCalib.dates,FL,'*')
#
#for j in range(len(np.array(pks[0]).T[0])):
#    plt.plot(FlowCalib.dates[np.array(pks[0]).T[0][j]],np.array(pks[0]).T[1][j],'ro')
#for j in range(len(np.array(pks[1]).T[0])):
#    plt.plot(FlowCalib.dates[np.array(pks[1]).T[0][j]],np.array(pks[1]).T[1][j],'go')
#
#plt.show()
#
#
#def POT(Timeserie,kp,f,qlim):
#    if len(v) != len(x):
#        sys.exit('Input vectors v and x must have same length')
