# -*- coding: utf-8 -*-
from .. import RepRepStats

     
from contracts import contract
import numpy as np


@RepRepStats.reduction
def all(x):  # @ReservedAssignment
    """ %s := %s """
    return x

@RepRepStats.reduction
def one(x):  # @ReservedAssignment
    """ %s := Unique value of %s """
    if len(x) != 1:
        raise ValueError('Expected a unique value, got %s.' % len(x))
    return x[0]

@RepRepStats.reduction
def num(x):  # @ReservedAssignment
    """ n%s := Number of samples of %s"""
    return len(x)

def notnone(x):
    return [a for a in x if a is not None]

@RepRepStats.reduction
def min(x):  # @ReservedAssignment
    """ min(%s) := Minimum of %s """
    x = notnone(x)
    return np.nanmin(x)

@RepRepStats.reduction
def max(x):  # @ReservedAssignment
    """ max(%s) := Maximum of %s """
    x = notnone(x)
    return np.nanmax(x)

@RepRepStats.reduction
def mean(x):
    """ E\{%s\} := Average %s """
    from scipy.stats.stats import nanmean
    x = notnone(x)
    return nanmean(x)

@RepRepStats.reduction
def stddev(x):
    """ std\{%s\} := Standard deviation of %s """
    from scipy.stats.stats import nanstd
    x = notnone(x)
    return nanstd(x)

@RepRepStats.reduction
@contract(a='array[N]', returns='tuple(number, number)')
def mean_std(a):
    """ mean,std\{%s\} := mean and standard deviation of %s """
    a = np.array(a)
    return (np.mean(a), np.std(a))

@RepRepStats.reduction
@contract(a='array[N]|list', returns='tuple(number, number, number)')
def min_mean_max(a):
    """ b\{%s\} := Min, mean and max of %s """
    a = np.asarray(a, dtype='float')  # converts bool
    from scipy.stats.stats import nanmean
    return (np.nanmin(a), nanmean(a), np.max(a))

