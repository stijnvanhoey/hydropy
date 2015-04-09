# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 12:02:28 2014

@author: stvhoey
"""

def get_baseflow_chapman(flowserie, recession_time):
    """

    Parameters
    ----------
    flowserie :  pd.TimeSeries
        River discharge flowserie
    recession_time : float [0-1]
        recession constant

    Notes
    ------
    $$Q_b(i) = \frac{k}{2-k}Q_b(i-1) + \frac{1-k}{2-k}Q(i)$$

    """

    if not isinstance(flowserie, pd.TimeSeries):
        raise Exception("Not a pd.TimeSerie as input")

    secterm = (1.-recession_time)*flowserie/(2.-recession_time)

    baseflow = np.empty(flowserie.shape[0])
    for i, timestep in enumerate(baseflow):
        if i == 0:
            baseflow[i] = 0.0
        else:
            baseflow[i] = recession_time*baseflow[i-1]/(2.-recession_time) + \
                            secterm.values[i]
    return pd.TimeSeries(baseflow, index = flowserie.index)

def get_baseflow_boughton(flowserie, recession_time, baseflow_index):
    """

    Parameters
    ----------
    flowserie :  pd.TimeSeries
        River discharge flowserie
    recession_time : float [0-1]
        recession constant
    baseflow_index : float

    Notes
    ------
    $$Q_b(i) = \frac{k}{1+C}Q_b(i-1) + \frac{C}{1+C}Q(i)$$

    """

    if not isinstance(flowserie, pd.TimeSeries):
        raise Exception("Not a pd.TimeSerie as input")

    parC =  baseflow_index

    secterm = parC*flowserie/(1 + parC)

    baseflow = np.empty(flowserie.shape[0])
    for i, timestep in enumerate(baseflow):
        if i == 0:
            baseflow[i] = 0.0
        else:
            baseflow[i] = recession_time*baseflow[i-1]/(1 + parC) + \
                            secterm.values[i]
    return pd.TimeSeries(baseflow, index = flowserie.index)

def get_baseflow_ihacres(flowserie, recession_time, baseflow_index, alfa):
    """

    Parameters
    ----------
    flowserie :  pd.TimeSeries
        River discharge flowserie
    recession_time : float [0-1]
        recession constant

    Notes
    ------
    $$Q_b(i) = \frac{k}{1+C}Q_b(i-1) + \frac{C}{1+C}[Q(i)+\alpha Q(i-1)]$$

    $\alpha$ < 0.
    """

    if not isinstance(flowserie, pd.TimeSeries):
        raise Exception("Not a pd.TimeSerie as input")

    parC =  baseflow_index

    secterm = parC/(1 + parC)

    baseflow = np.empty(flowserie.shape[0])
    for i, timestep in enumerate(baseflow):
        if i == 0:
            baseflow[i] = 0.0
        else:
            baseflow[i] = recession_time*baseflow[i-1]/(1 + parC) + \
                            secterm*(flowserie.values[i] + \
                                        alfa*flowserie.values[i-1])
    return pd.TimeSeries(baseflow, index = flowserie.index)