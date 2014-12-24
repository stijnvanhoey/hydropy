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

def Montharray(FlowSerie,ChMont='Jan', lijst=False):
    '''
    returns array only of preferred month, no time-information
    '''
    #Extracts all the data from a specific month over all the years of the timeserie
    #Input must be timeserie (sckits.timeseries) !!
    RowMonth_day=FlowSerie.convert('M')
    StrMonth=RowMonth_day.dates.tostring()
    Months=[]
    i=0
    for maand in StrMonth:
        if maand[0:3] == ChMont:
            tempt=RowMonth_day[i].compressed().tolist()
            Months=Months+tempt
        i=i+1
    FlowMonth=np.array(Months)
    if lijst == False:
        return FlowMonth
    else:
        return Months
        
def MonthSerie(FlowSerieIn,chmonth='Jan'):
    '''
    returns array only of preferred month, no time-information
    chmont: integer 1-12 ro 3Char-month with first capital
    '''    
    FlowSerieIn.unshare_mask()
    FlowSerie=FlowSerieIn.copy()
    
    #Extracts all the data from a specific month over all the years of the timeserie
    #Input must be timeserie (sckits.timeseries) !!
    mdict=dict((v,k) for k,v in enumerate(calendar.month_abbr))
    if isinstance(chmonth,int):
        if chmonth > 0 and chmonth < 13:
            monthsel=chmonth
        else:
            raise Exception('Choose monthnumber between 1 and 12')
    elif isinstance(chmonth,str):
        if len(chmonth)==3 and chmonth[0].isupper():
            if chmonth in mdict:
                monthsel = mdict[chmonth]
            else:
                raise Exception('Month not in dictionary')
        else:
            raise Exception('Use three letter month abbreviation with first letter capital')           
    else:
        raise Exception('Use integer of 3letter month abbreviation')

    #old version                
#    mmask=FlowSerie.month==monthsel
#    for i in range(FlowSerie.size):
#        if not mmask[i]:
#            FlowSerie[i]=ma.masked
    #new version
    FlowSerie=ma.masked_where(FlowSerie.month <> monthsel, FlowSerie)
    
    return FlowSerie,FlowSerie.mask.copy()

def SeasonArray(Floweff,chseason='Spring'):
    '''
    returns array only of preferred season, no time-information
    '''
    #Extracts all the data from a specific season over all the years of the timeserie
    if chseason =='Winter':
        FlowSerie1=Montharray(Floweff,ChMont='Dec',lijst=True)
        FlowSerie2=Montharray(Floweff,ChMont='Jan',lijst=True)
        FlowSerie3=Montharray(Floweff,ChMont='Feb',lijst=True)
        FlowSerie=np.array(FlowSerie1+FlowSerie2+FlowSerie3)
        return FlowSerie

    if chseason == 'Spring':
        FlowSerie1=Montharray(Floweff,ChMont='Mar',lijst=True)
        FlowSerie2=Montharray(Floweff,ChMont='Apr',lijst=True)
        FlowSerie3=Montharray(Floweff,ChMont='May',lijst=True)
        FlowSerie=np.array(FlowSerie1+FlowSerie2+FlowSerie3)
        return FlowSerie

    if chseason == 'Summer':
        FlowSerie1=Montharray(Floweff,ChMont='Jun',lijst=True)
        FlowSerie2=Montharray(Floweff,ChMont='Jul',lijst=True)
        FlowSerie3=Montharray(Floweff,ChMont='Aug',lijst=True)
        FlowSerie=np.array(FlowSerie1+FlowSerie2+FlowSerie3)
        return FlowSerie

    if chseason == 'Fall':
        FlowSerie1=Montharray(Floweff,ChMont='Sep',lijst=True)
        FlowSerie2=Montharray(Floweff,ChMont='Oct',lijst=True)
        FlowSerie3=Montharray(Floweff,ChMont='Nov',lijst=True)
        FlowSerie=np.array(FlowSerie1+FlowSerie2+FlowSerie3)
        return FlowSerie  

def SeasonSerie(FlowSerie,ChSeason='Spring'):
    '''
    returns array only of preferred season, no time-information
    '''
    #Extracts all the data from a specific season over all the years of the timeserie
    ftemp=FlowSerie.copy()
    if ChSeason =='Winter':
        ftemp=ma.masked_where(FlowSerie.month>11, ftemp)
        ftemp=ma.masked_where(FlowSerie.month<3, ftemp)    
        FlowSerie=ma.masked_where(ftemp.mask==False, FlowSerie) 
        return FlowSerie,FlowSerie.mask.copy()

    #for these months the ftemp isn't necessary!!
    if ChSeason == 'Spring': #DEES IS GOE, NU DE ANDERE NOG
        ftemp=ma.masked_where(FlowSerie.month>5, ftemp)
        ftemp=ma.masked_where(FlowSerie.month<3, ftemp)    
        FlowSerie=ma.masked_where(ftemp.mask==True, FlowSerie) 
        return FlowSerie,FlowSerie.mask.copy()

    if ChSeason == 'Summer':
        ftemp=ma.masked_where(FlowSerie.month>8, ftemp)
        ftemp=ma.masked_where(FlowSerie.month<6, ftemp)    
        FlowSerie=ma.masked_where(ftemp.mask==True, FlowSerie) 
        return FlowSerie,FlowSerie.mask.copy()

    if ChSeason == 'Fall':
        ftemp=ma.masked_where(FlowSerie.month>11, ftemp)
        ftemp=ma.masked_where(FlowSerie.month<9, ftemp)    
        FlowSerie=ma.masked_where(ftemp.mask==True, FlowSerie) 
        return FlowSerie,FlowSerie.mask.copy()          

def invertMask(TSIn):
    TSIn.unshare_mask()
    TSOut=TSIn.copy()
    for i in range(TSOut.mask.size):
        if TSOut.mask[i]==True:
            TSOut.mask[i]=False
        else:
            TSOut.mask[i]=True
    return TSOut,TSOut.mask.copy()

def getRecess(FlowInM):
    '''
    Returns Timeserie with the non-recesssion parts masked out and a copy of this mask
    start with all FAlse
    '''
    #PUT ALL FALSES    
#    FlowInM.mask = ma.nomask
    FlowInM.unshare_mask()  #Important for masked arrays!
    FlowIn=FlowInM.copy()

    #Give the climb/notvlimb value a start
    if FlowIn.data[1]>FlowIn.data[0]:
        climb=True
    else:
        climb=False

    for i in range(1,FlowIn.size-1):
        if FlowIn[i] is ma.masked:
            continue
        else:
            if FlowIn.data[i]==FlowIn.data[i-1]:
                if climb==True:
                    FlowIn[i]=ma.masked #wordt afgeraden doo: beter:x[0] = ma.masked
#                else:
#                    FlowIn.mask[i]=False
            elif FlowIn.data[i]>FlowIn.data[i-1]:
                FlowIn[i]=ma.masked
                climb=True
            else:
#                FlowIn.mask[i]=False
                climb=False
    return FlowIn,FlowIn.mask.copy()

def getClimb(FlowInM):
    '''
    Returns Timeserie with the recesssion parts masked out and a copy of this mask
    '''
    FlowIn=FlowInM.copy()

    FlowRec,recmask=getRecess(FlowIn)
    FlowRec.unshare_mask()
    FlowLimb,climbmask=invertMask(FlowRec)
    FlowLimb.unshare_mask()

    return FlowLimb,climbmask

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
















