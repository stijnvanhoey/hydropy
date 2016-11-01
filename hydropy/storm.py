# -*- coding: utf-8 -*-
"""
Hydropy package

@author: Stijn Van Hoey
"""
from __future__ import absolute_import, print_function

import datetime

import numpy as np
import pandas as pd
from pandas.tseries.offsets import DateOffset, Day, Week, Hour, Minute

from matplotlib.ticker import LinearLocator
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
mpl.rcParams['mathtext.default'] = 'regular'


def selectstorms(flowserie, rainserie, number_of_storms=3,
                 min_period_in_between=7, search_period=7,
                 drywindow=96):
    """ (pd.DataFrame, pd.DataFrame) -> List
    Easy storm selection process, based on the maximum flows measured
    in the given timeserie of flow measurements.

    To define the startdate of the storm, 24h no rain before the Qmax is
    searched for. The end date is found by checking the
    flow at the startdate (Qbase) and searching the moment after Qmax with
    the same flow within the first 2 weeks.
    If none is found, relaxation (1.1*Qbase; 1.2*Qbase,...)
    until a moment is found.

    Parameters
    ----------
    flowserie : pd.Series
        Pandas Series with the date in the index
    rainserie : pd.Series
        Pandas Series with the date in the index
    number_of_storms : int
        Number of storms you want to select
    min_period_in_between : int (days)
        Minimum number of days in between to selected storms
    search_period : int (days)
        Period to look for the start of the storm, when rain started
    drywindow : int
        Number of timesteps to check for no-rain
    """
    if not isinstance(flowserie, pd.Series):
        raise Exception('flowserie is a single data Series')
    if not isinstance(rainserie, pd.Series):
        raise Exception('rainserie is a single data Series')

    # fill na values with very low (negative) value
    temp = flowserie.fillna(value=-777.).copy()
    # sort the whole array
    try:
        temp = temp.sort(temp.columns.tolist(), ascending=False)
    # TODO: set a specific exception to react to.
    except:
        temp.sort(ascending=False)

    # find in the index three periods which are at least given number
    # of days from each other
    # after three concurrences, save these dates
    stormmax = [temp.index[0]]  # first element is a selected storm
    i = 1
    while len(stormmax) < number_of_storms:
        # check for each period
        alldif = True
        for stormdate in stormmax:
            if abs(temp.index[i] - stormdate) \
                    < datetime.timedelta(days=min_period_in_between):
                alldif = False
        # if new stormperiod, select
        if alldif:
            stormmax.append(temp.index[i])
        i += 1

    selstorms = []
    for storm in stormmax:
        # FIND DRY DAY WEEK BEFORE
        # select period before storm (1 week)
        presearchperiod = datetime.timedelta(days=search_period)
        temp1 = rainserie[storm - presearchperiod:storm]
        temp1 = pd.rolling_sum(temp1, window=drywindow, center=False)
        # zero value means the preceding 24hours no rain: so, closest zeros
        # to the date itself -24h are selected
        if rainserie.ndim == 2:
            temp1 = temp1.min(axis=1)
        tempdates = temp1[temp1 < 0.001].index.tolist()
        if len(tempdates) == 0:
            raise Exception('Decrease drywindow period containing no rain.')

        date_arg = np.argmin([abs(times - storm) for times in tempdates])
        startstormdate = tempdates[date_arg] - Day()

        # Get the flow value of the storm and when it is found again + 1 Day
        temp2a = flowserie[startstormdate:startstormdate + Week()*2]

        # only if multiple columns
        if flowserie.ndim == 2:
            temp2 = temp2a.max(axis=1)
        else:
            temp2 = temp2a

        flowbase = temp2.ix[startstormdate]
        lowerafterstorm = temp2[temp2 < flowbase][storm + Day():]
        if lowerafterstorm.size == 0:
            print('Lower initial flow not found again...test with mean...')
            if flowserie.ndim == 2:
                temp2 = temp2a.mean(axis=1)
            else:
                temp2 = temp2a
            flowbase = temp2.ix[startstormdate]
            lowerafterstorm = temp2[temp2 < flowbase][storm + Day():]
        cnt = 1
        while lowerafterstorm.size == 0:
            print('...    still not working; relaxing conditions...',
                  cnt*10, '% of minimal after storm incorporated')
            flowbase = flowbase + 0.1*flowbase
            lowerafterstorm = temp2[temp2 < flowbase][storm + Day():]
            cnt += 1
        endstormdate = lowerafterstorm.index[0]

        # add to selected storms
        selstorms.append({'startdate': startstormdate,
                          'enddate': endstormdate})

    return selstorms


def _control_dayhour(timestamp):
    """pd.TimeStamp -> int

    Help function for editing the date representation of the plots
    """
    if timestamp.hour == 0 and timestamp.minute == 0:
        return 0
    else:
        return 1


def _getsize(nrows):
    """int -> int

    propose height of the figure based on number of rows
    """
    size_dict = {1: 6, 2: 6, 3: 8, 4: 8, 5: 10, 6: 12}
    return size_dict[nrows]


def _add_labels_above(ax0, fig, flowdim, raindim):
    """ matplotlib.axes -> None

    """
    bbox = ax0.get_position()
    rainlabel = ax0.text(bbox.x0 + bbox.width,
                         bbox.y0 + bbox.height, r"Rain ($mm$)",
                         transform=fig.transFigure,
                         verticalalignment="bottom",
                         horizontalalignment="right")
    flowlabel = ax0.text(bbox.x0, bbox.y0 + bbox.height,
                         r"Flow ($m^3s^{-1}$)",
                         transform=fig.transFigure,
                         verticalalignment="bottom",
                         horizontalalignment="left")
    if flowdim == 1:
        flowlabel.set_color('#08519c')
    if raindim == 1:
        rainlabel.set_color('#6baed6')


def _make_comparable(axes):
    """axes  -> None

    updates the y-bound of the subplot, giving them all the bounds of the
    largest

    only used for the rain-flow combined subplots configuration within a
    gridspec environment
    """
    # check the configuration
    if axes[0].get_subplotspec().get_gridspec().get_height_ratios():
        nplots = int(len(axes)/2.)
        ymaxes = [max(axs.get_yticks()) for axs in axes]
        rainmax = max(ymaxes[::2])
        flowmax = max(ymaxes[1::2])
        newmaxes = [rainmax, flowmax]*nplots
        for axs, nmax in zip(axes, newmaxes):
            axs = axs.set_ybound(upper=nmax)
    else:
        ymaxes = [max(axs.get_yticks()) for axs in axes[1:]]
        flowmax = max(ymaxes)
        for axs in axes[1:]:
            axs = axs.set_ybound(upper=flowmax)


def plotstorms(flowserie, rainserie, selected_storm,
               tsfreq=None, tsfrequnit=None,
               make_comparable=False,
               period_title=False):
    """
    Plot Flow-Rain plots for every storm period selected,

    optimal sizes and configuration done for 1 till 5 subplots (storms)
    """
    if len(selected_storm) > 6:
        raise Exception('Split plotting up in multiple figures')
    fig = plt.figure(facecolor='white',
                     figsize=(12, _getsize(len(selected_storm))))
    gs0 = gridspec.GridSpec(len(selected_storm), 1)
    gs0.update(hspace=0.35)

    for j, storm in enumerate(selected_storm):
        gs00 = gridspec.GridSpecFromSubplotSpec(2, 1,
                                                subplot_spec=gs0[j],
                                                hspace=0.0,
                                                height_ratios=[2, 4])
        # RAIN PLOT
        ax0 = fig.add_subplot(gs00[0])
        ax0.plot(
            rainserie[storm['startdate']: storm['enddate']].index.to_pydatetime(),
            rainserie[storm['startdate']: storm['enddate']].values,
            linestyle='steps')

        # FLOW PLOT
        stormflow = flowserie[storm['startdate']: storm['enddate']]
        ax1 = fig.add_subplot(gs00[1], sharex=ax0)
        ax1.plot(stormflow.index.to_pydatetime(), stormflow.values,
                 label=r" Measured Flow ($m^3s^{-1}$)")
        # if single plots of flow/rain -> set specific color
        if flowserie.ndim == 1:
            ax1.lines[0].set_color('#08519c')
        if rainserie.ndim == 1:
            ax0.lines[0].set_color('#6baed6')

        # ADAPT ticks for storm-conditions (less than a month timeseries)
        ax0.yaxis.set_major_locator(LinearLocator(3))
        ax1.yaxis.set_major_locator(LinearLocator(3))

        ax1.xaxis.set_minor_locator(mpl.dates.DayLocator())
        ax1.xaxis.set_minor_formatter(mpl.dates.DateFormatter('%d'))
        ax1.xaxis.set_major_locator(mpl.dates.MonthLocator(bymonthday=
                                    [1, storm['startdate'].day +
                                    _control_dayhour(storm['startdate'])]))
        ax1.xaxis.set_major_formatter(mpl.dates.DateFormatter('\n %b %Y'))

        # Add the labels of the different flows
        if j == 0:
            _add_labels_above(ax0, fig, flowserie.ndim, rainserie.ndim)

        # Print the start and end period as title above subplots
        if period_title:
            ax0.set_title(storm['startdate'].strftime("%d/%m/%y") + " - " +
                          storm['enddate'].strftime("%d/%m/%y"),
                          fontweight='bold', fontsize=12)

        # Looks of the rainplot
        ax0.set_xlabel('')
        ax0.invert_yaxis()
        ax0.yaxis.tick_right()
        ax0.spines['bottom'].set_visible(False)
        ax0.spines['top'].set_visible(False)
        plt.setp(ax0.get_xminorticklabels(), visible=False)
        plt.setp(ax0.get_xmajorticklabels(), visible=False)
        plt.setp(ax0.get_xminorticklabels(), visible=False)

        # looks of the flowplot
        ax1.spines['top'].set_visible(False)
        ax1.spines['bottom'].set_visible(False)
        ax1.set_xlabel('')

    plt.draw()
    all_axes = fig.get_axes()

    # Give all the subplots the same y-bounds
    if make_comparable:
        _make_comparable(all_axes)

    return fig, all_axes
