# -*- coding: utf-8 -*-
from contracts import contract

import numpy as np

from . import get_scaled_values
from .. import get_matplotlib, get_pylab_instance


@contract(returns='array[HxWx4](uint8)')
def value2rgb(x, vmin=0, vmax=1, cmap='jet'):
    ''' Asssumes x is in [0,1]. '''
    matplotlib = get_matplotlib()
    pylab = get_pylab_instance()
    isint = matplotlib.is_interactive()
    if isint:
        matplotlib.set_interactive(False)  # @UndefinedVariable
    f = pylab.figure()
    # m = f.gca().imshow(x, vmin=vmin, vmax=vmax, 
    # cmap=pyplot.cm.get_cmap(cmap))
    mcmap = pylab.cm.get_cmap(cmap)
    if mcmap is None:
        raise Exception('Unknown cmap %r.' % cmap)
    m = pylab.figimage(x, 0, 0, vmin=vmin, vmax=vmax, cmap=mcmap)
    m.set_cmap(mcmap)
    rgb = m.to_rgba(x)
    rgb = (rgb * 255).astype('uint8')
    pylab.close(f)
    return rgb


@contract(value='array[HxW],H>0,W>0',
          max_value='None|number',
          min_value='None|number',
          skim='>=0,<=90',
          nan_color='color_spec',
          inf_color='color_spec',
          flat_color='color_spec',
          properties='None|map')
def filter_colormap(value,
                   cmap='jet',
                   min_value=None, max_value=None,
                   nan_color=[1, 0.6, 0.6],
                   inf_color=[0.6, 1, 0.6],
                   flat_color=[0.5, 0.5, 0.5],
                   skim=0,
                   properties=None):

    """
    
      shape = grid.get_map().shape
    xb = np.linspace(0, shape[0] * 1.0, shape[0] / res)
    yb = np.linspace(0, shape[1] * 1.0, shape[1] / res)
    X, Y = np.meshgrid(xb, yb)
    values = F(X,Y)
    values_rgb = filter_colormap(values, cmap='jet')
    pylab.imshow(values_rgb, extent=(xb[0], xb[-1], yb[0], yb[-1]))


    
    """
    scaled = get_scaled_values(value,
                               min_value=min_value, max_value=max_value,
                               skim=skim)

    if scaled['flat']:
        rgb = get_solid(value.shape, flat_color)
    else:
        rgba = value2rgb(scaled['scaled01'], cmap=cmap)
        rgb = rgba[:, :, :3]
        # TODO: clip?
        mark_values(rgb, scaled['isinf'], inf_color)
        mark_values(rgb, scaled['isnan'], nan_color)

    if properties is not None:
        properties['min_value'] = scaled['min_value']
        properties['max_value'] = scaled['max_value']
        properties['nan_color'] = nan_color
        properties['flat_color'] = flat_color
        properties['inf_color'] = inf_color
        properties.update(scaled)
        bar_shape = (512, 128)
        bar = np.vstack([np.linspace(0, 1, bar_shape[0])] * bar_shape[1]).T
        properties['color_bar'] = value2rgb(bar, cmap=cmap)

    return rgb


@contract(rgb='array[HxWx3](uint8)', which='array[HxW]', color='color_spec')
def mark_values(rgb, which, color):
    for u in [0, 1, 2]:
        col = rgb[:, :, u]
        col[which] = color[u] * 255
        rgb[:, :, u] = col


@contract(shape='tuple((int,H),(int,W))', color='color_spec',
          returns='array[HxWx3](uint8)')
def get_solid(shape, color):
    res = np.zeros((shape[0], shape[1], 3), dtype='uint8')
    for u in [0, 1, 2]:
        res[:, :, u] = color[u] * 255
    return res
