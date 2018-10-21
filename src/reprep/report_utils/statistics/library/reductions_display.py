# -*- coding: utf-8 -*-
from contracts import contract
from .. import RepRepStats


@RepRepStats.reduction_display
@contract(s='tuple(number, number)', returns='str')
def mean_std_display(s):
    mean, std = s
    return '%s +/- %s' % (mean, std)


@RepRepStats.reduction_display
@contract(s='tuple(number, number, number)', returns='str')
def min_mean_max_s(s):
    a, b, c = s
    return '(%s) %s (%s)' % (a, b, c)


@RepRepStats.reduction_display
def string(s):
    return str(s)


@RepRepStats.reduction_display
def f(s):
    """ Format as a float number ('f' formatter) """
    return '%f' % s


@RepRepStats.reduction_display
def f5(s):
    """ Format as a float number ('f' formatter) with 5 digits """
    return '%.5f' % s

@RepRepStats.reduction_display
def f4(s):
    """ Format as a float number ('f' formatter) with 4 digits """
    return '%.4f' % s

@RepRepStats.reduction_display
def f3(s):
    """ Format as a float number ('f' formatter) with 3 digits """
    return '%.3f' % s

@RepRepStats.reduction_display
def f2(s):
    """ Format as a float number ('f' formatter) with 2 digits """
    return '%.2f' % s

@RepRepStats.reduction_display
def f1(s):
    """ Format as a float number ('f' formatter) with 1 digits """
    return '%.1f' % s

@RepRepStats.reduction_display
def perc(s):
    """ Format as a percentual """ 
    return '%d%%' % (100 * s)

@RepRepStats.reduction_display
def g(s):
    """ Format as a float number ('g' formatter) """
    return '%g' % s

@RepRepStats.reduction_display
def d(s):
    """ Format as an integer ('d' formatter) """
    return '%d' % s
