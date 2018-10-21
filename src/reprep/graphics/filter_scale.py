# -*- coding: utf-8 -*-
from . import skim_top
from contracts import contract
from numpy import maximum, minimum, zeros
import numpy as np



@contract(value='array[HxW],H>0,W>0',
          max_value='None|number',
          min_value='None|number',
          skim='>=0,<=90',
          min_color='color_spec',
          nan_color='color_spec',
          max_color='color_spec',
          flat_color='color_spec',
          properties='None|map')
def scale(value, min_value=None, max_value=None,
                 min_color=[1, 1, 1],
                 max_color=[0, 0, 0],
                 nan_color=[1, 0.6, 0.6],
                 flat_color=[0.5, 0.5, 0.5],
                 skim=0,
                 properties=None):
    """ 
        Provides a RGB representation of the values by interpolating the range 
        [min(value),max(value)] into the colorspace [min_color, max_color].
        
        Input: a numpy array with finite values squeeze()able to (W,H).
        
        Configuration:
        
        - ``min_value``: If specified, this is taken to be the threshold. 
                         Everything below min_value is considered to 
                         be equal to min_value.
        - ``max_value``: Optional upper threshold.
        - ``min_color``: color associated to minimum value. 
        - ``max_color``: color associated to maximum value. 
        - ``nan_color``: color associated to nan/inf values. 
       
        If all valid elements have the same value, their color will be 
        ``flat_color``.
        
        Returns:  a (W,H,3) numpy array with dtype uint8 
        representing a RGB image.
      
    """
    value = value.astype('float32')
    H, W = value.shape
    
#    if value.ndim > 2:
#        value = value.squeeze()

    if value.dtype == np.dtype('uint8'):  # todo: or other integers
        value = value.astype('float32')
        
    isnan = np.logical_not(np.isfinite(value))

    if skim != 0:
        value = skim_top(value, skim)

    if max_value is None:
        max_value = np.nanmax(value)
    if min_value is None:
        min_value = np.nanmin(value)
    # but what about +- inf?

    if properties is not None:
        properties['min_value'] = min_value
        properties['max_value'] = max_value
        properties['min_color'] = min_color
        properties['max_color'] = max_color
        properties['nan_color'] = nan_color
        bar_shape = (512, 128)
        bar = np.vstack([np.linspace(0, 1, bar_shape[0])] * bar_shape[1]).T
        properties['color_bar'] = interpolate_colors(bar, min_color, max_color)

    if max_value == min_value or \
      (not np.isfinite(min_value)) or \
      (not np.isfinite(max_value)):
        result = zeros((H, W, 3), dtype='uint8')
        result[:, :, 0] = flat_color[0]  # TODO: write something?
        result[:, :, 1] = flat_color[1]
        result[:, :, 2] = flat_color[2]
        mark_nan(result, isnan, nan_color)
        return result

    assert np.isfinite(min_value)
    assert np.isfinite(max_value)

    value01 = (value - min_value) / (max_value - min_value)

    # Cut at the thresholds
    value01 = maximum(value01, 0)
    value01 = minimum(value01, 1)
    value01[isnan] = 0.5  # any value
    result = interpolate_colors(value01, min_color, max_color)
    mark_nan(result, isnan, nan_color)
    return result


def mark_nan(result, isnan, nan_color):
    for u in [0, 1, 2]:
        col = result[:, :, u]
        col[isnan] = nan_color[u] * 255
        result[:, :, u] = col


def interpolate_color(value, a, b):
    return 255 * ((1 - value) * a + value * b)


@contract(value='array[HxW]((float32|float64),>=0,<=1)',
          min_colors='color_spec', max_colors='color_spec',
          returns='array[HxWx3](uint8)')
def interpolate_colors(value, min_colors, max_colors):
    result = zeros((value.shape[0], value.shape[1], 3), dtype='uint8')
    for u in [0, 1, 2]:
        result[:, :, u] = interpolate_color(value, min_colors[u],
                                            max_colors[u])
    return result
