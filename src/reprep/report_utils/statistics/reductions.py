from . import np, contract
from reprep.report_utils.statistics import RepRepStats
from scipy.stats.stats import nanmean, nanstd
     

@RepRepStats.reduction
def all(x): #@ReservedAssignment
    """ %s := %s """
    return x

@RepRepStats.reduction
def one(x): #@ReservedAssignment
    """ %s := Unique value of %s """
    if len(x) != 1:
        raise ValueError('Expected a unique value, got %s.' % len(x))
    return x[0]

@RepRepStats.reduction
def num(x): #@ReservedAssignment
    """ n%s := Number of samples of %s"""
    return len(x)

def notnone(x):
    return [a for a in x if a is not None]

@RepRepStats.reduction
def min(x): #@ReservedAssignment
    """ min(%s) := Minimum of %s """
    x = notnone(x)
    return np.nanmin(x)

@RepRepStats.reduction
def max(x): #@ReservedAssignment
    """ max(%s) := Maximum of %s """
    x = notnone(x)
    return np.nanmax(x)

@RepRepStats.reduction
def mean(x):
    """ E\{%s\} := Average %s """
    x = notnone(x)
    return nanmean(x)

@RepRepStats.reduction
def stddev(x):
    """ std\{%s\} := Standard deviation of %s """
    x = notnone(x)
    return nanstd(x)

@RepRepStats.reduction
@contract(a='array[N]', returns='tuple(number, number)')
def mean_std(a):
    """ mean,std\{%s\} := mean and standard deviation of %s """
    a = np.array(a)
    return (np.mean(a), np.std(a))

@RepRepStats.reduction
@contract(a='array[N]', returns='tuple(number, number, number)')
def min_mean_max(a):
    """ b\{%s\} := Min, mean and max of %s """
    a = np.array(a)
    return (np.nanmin(a), nanmean(a), np.max(a))


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

