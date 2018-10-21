# -*- coding: utf-8 -*-
from contracts import contract
import numpy as np


@contract(a='array', top_percent='>=0,<=90')
def skim_top(a, top_percent):
    ''' Cuts off the top percentile '''
    threshold = np.percentile(a.flat, 100 - top_percent)
    return np.minimum(a, threshold)


@contract(value='array[HxW],H>0,W>0',
          max_value='None|number',
          min_value='None|number',
          skim='>=0,<=90')
def get_scaled_values(value, min_value=None, max_value=None, skim=0):
    '''
        Returns dictionary with entries:
        - value01       Values in [0, 1], no inf, nan, where it is set 0.5.
        - isnan         Values were NaN.
        - isinf         Values were +-Inf
        - isfin         Values weren't Inf or NaN
        - clipped_ub    Values were clipped 
        - clipped_lb
        - flat          Boolean if there wasn't a range
        - min_value
        - max_value
    '''
    value = value.copy().astype('float32')

    isfin = np.isfinite(value)
    isnan = np.isnan(value)
    isinf = np.isinf(value)

    if skim != 0:
        # TODO: skim bottom?
        value = skim_top(value, skim)

    if max_value is None or min_value is None:
        value[value == +np.Inf] = -np.Inf
        value[value == -np.Inf] = -np.Inf
        vmax = np.nanmax(value)
        value[value == +np.Inf] = +np.Inf
        value[value == -np.Inf] = +np.Inf
        vmin = np.nanmin(value)
        bounds = (vmin, vmax)

    if max_value is None:
        max_value = bounds[1]
    if min_value is None:
        min_value = bounds[0]
    # but what about +- inf?

    assert np.isfinite(min_value)
    assert np.isfinite(max_value)

    # Put values for filling in
    a_value = min_value
    value[isinf] = a_value
    value[isnan] = a_value

    if max_value == min_value:
        scaled = np.empty_like(value)
        scaled.fill(a_value)
        flat = True
    else:
        scaled = (value - min_value) * (1.0 / (max_value - min_value))
        flat = False

    clipped_ub = scaled > 1
    clipped_lb = scaled < 0

    # Cut at the thresholds
    scaled01 = np.maximum(scaled, 0)
    scaled01 = np.minimum(scaled01, 1)

    return dict(
                scaled01=scaled01,
                isnan=isnan,
                isinf=isinf,
                isfin=isfin,
                flat=flat,
                min_value=min_value,
                max_value=max_value,
                clipped_ub=clipped_ub,
                clipped_lb=clipped_lb
                )

