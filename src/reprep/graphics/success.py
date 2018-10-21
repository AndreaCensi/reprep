# -*- coding: utf-8 -*-
from contracts import contract
import numpy as np


@contract(values='array[HxW]',
          colors='list[>=1](tuple(a,(b,b>a),seq[4](number)))')
def colormap_rgba(values, colors,
                  invalid_color=[255, 255, 0, 255],
                  nan_color=[0, 0, 0, 0]):
    ''' colors = [ (min, max, [r,g,b,a]),... ] '''
    h, w = values.shape
    res = np.zeros(shape=(h, w, 4), dtype='uint8')
    for i in range(h):
        for j in range(w):
            chosen = invalid_color
            val = values[i, j]
            for vmin, vmax, color in colors:
                if vmin <= val <= vmax:
                    chosen = color
                    break
            if np.isnan(val):
                chosen = nan_color
            res[i, j, :] = chosen
    return res


@contract(value='array[HxW](>=0,<=1)')
def colorize_success(value):
    red = [255, 0, 0, 255]
    magenta = [186, 50, 50, 255]
    yellow = [255, 255, 0, 255]
    orange = [255, 164, 18, 255]
    blue = [0, 50, 255, 255]
    bluegreen = [0, 150, 50, 255]
    darkgreen = [0, 200, 0, 255]
    green = [0, 255, 0, 255]

    colors = [(0, 0.001, red), (0.001, 0.05, magenta), (0.05, 0.25, yellow),
              (0.25, 0.50, orange), (0.5, 0.75, blue), (0.75, 0.95, bluegreen),
              (0.95, 0.99, darkgreen), (0.99, 1, green)]
    rgba = colormap_rgba(value, colors)
    return rgba
