# -*- coding: utf-8 -*-
import numpy as np


def plot_horizontal_line(pylab, y, *args, **kwargs):
    ''' Plots an horizontal line across the plot using current bounds. '''
    a = pylab.axis()
    pylab.plot([a[0], a[1]], [y, y], *args, **kwargs)

def plot_vertical_line(pylab, x, *args, **kwargs):
    ''' Plots a vertical line across the plot using current bounds. '''
    a = pylab.axis()
    pylab.plot([x, x], [a[2], a[3]], *args, **kwargs)


def y_axis_balanced(pylab, extra_space=0.1, show0=True):
    a = pylab.axis()
    y_max = a[3]
    y_min = a[2]
    D = np.max([np.abs(y_max), np.abs(y_min)])
    D *= (1 + extra_space)
    pylab.axis((a[0], a[1], -D, +D))
    if show0:
        plot_horizontal_line(pylab, 0, 'k--')


def y_axis_positive(pylab, extra_space=0.1, show0=True):
    a = pylab.axis()
    y_max = a[3]
    y_min = -y_max * extra_space
    y_max *= (1 + extra_space)
    pylab.axis((a[0], a[1], y_min, y_max))
    if show0:
        plot_horizontal_line(pylab, 0, 'k--')


def x_axis_extra_space_right(pylab, fraction=0.1):
    a = pylab.axis()
    D = a[1] - a[0]
    extra = D * fraction
    pylab.axis((a[0], a[1] + extra, a[2], a[3]))


def y_axis_extra_space(pylab, extra_space=0.1):
    a = pylab.axis()
    D = a[3] - a[2]
    extra = D * extra_space
    pylab.axis((a[0], a[1], a[2] - extra, a[3] + extra))

def x_axis_extra_space(pylab, extra_space=0.1):
    a = pylab.axis()
    D = a[1] - a[0]
    extra = D * extra_space
    pylab.axis((a[0] - extra, a[1] + extra, a[2], a[3]))


def x_axis_balanced(pylab, extra_space=0.1):
    a = pylab.axis()
    D = a[1] - a[0]
    extra = D * extra_space
    pylab.axis((a[0] - extra, a[1] + extra, a[2], a[3]))


def x_axis_set(pylab, xmin, xmax):
    a = pylab.axis()
    pylab.axis((xmin, xmax, a[2], a[3]))


def y_axis_set(pylab, ymin, ymax):
    a = pylab.axis()
    pylab.axis((a[0], a[1], ymin, ymax))

def y_axis_set_min(pylab, ymin):
    a = pylab.axis()
    pylab.axis((a[0], a[1], ymin, a[3]))


def turn_all_axes_off(pylab):
    """ Turns everything off. (TODO) """
    axes = pylab.gca()
    axes.set_frame_on(False)
    pylab.setp(axes.get_xticklabels(), visible=False)
    pylab.setp(axes.get_yticklabels(), visible=False)
    axes.xaxis.offsetText.set_visible(False)
    axes.yaxis.offsetText.set_visible(False)
    axes.xaxis.set_ticks_position('none')
    axes.yaxis.set_ticks_position('none')
    for _, spine in axes.spines.items():
        spine.set_color('none')

