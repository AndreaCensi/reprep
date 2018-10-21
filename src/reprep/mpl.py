# -*- coding: utf-8 -*-
from reprep import logger

__all__ = ['get_matplotlib', 'get_pylab_instance']

class Global(object):
    my_pylab_instance = None
    matplotlib_error = None
    my_matplotlib = None
    loaded = False
    
def try_load_matplotlib():
    if Global.loaded:
        return
    
    # logger.info('Trying loading matplotlib')
    try:
        import matplotlib
    except ImportError as e:
        msg = ('Could not import matplotlib; some functionality will be '
               'disabled.')
        logger.warning(msg)
        Global.matplotlib_error = e
    else:
        # TODO: configure this
        if matplotlib.get_backend() != 'agg':
            matplotlib.use('agg')
        from matplotlib import pylab
        Global.my_pylab_instance = pylab
        Global.my_matplotlib = matplotlib

    Global.loaded = True
    
# Need to load this now, to set to the "agg" backend, otherwise
# we might fail in headless environment.
try_load_matplotlib()
    
def get_pylab_instance():
    try_load_matplotlib()
    if Global.my_pylab_instance is None:
        raise_error()

    return Global.my_pylab_instance

def get_matplotlib():
    try_load_matplotlib()
    if Global.my_matplotlib is None:
        raise_error()
        
    return Global.my_matplotlib

def raise_error():
    msg = ('Sorry, this functionality is not enabled because '
           'I could not import matplotlib (%s)' % Global.matplotlib_error)
    raise Exception(msg)
