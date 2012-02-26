from . import logger

__all__ = ['get_matplotlib', 'get_pylab_instance']
my_pylab_instance = None
matplotlib_error = None
my_matplotlib = None

try:
    import matplotlib
except ImportError as e:
    msg = ('Could not import matplotlib; some functionality will be '
           'disabled.')
    logger.warning(msg)
    matplotlib_error = e
else:
    # TODO: configure this
    if matplotlib.get_backend() != 'agg':
        matplotlib.use('agg')
    from matplotlib import pylab as my_pylab_instance
    my_matplotlib = matplotlib


def get_pylab_instance():
    if my_pylab_instance is None:
        raise_error()

    return my_pylab_instance


def get_matplotlib():
    if my_matplotlib is None:
        raise_error()
    return my_matplotlib


def raise_error():
    msg = ('Sorry, this functionality is not enabled because '
           'I could not import matplotlib (%s)' % matplotlib_error)
    raise Exception(msg)
