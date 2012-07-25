from ... import logger

try:
    import tables
except:
    logger.warning('No HDF support.')
else:
    __all__ = ['to_hdf', 'report_from_hdf']
    from .hdf1_rawdata import *
    from .hdf1_read import *
    from .hdf1_write import *
    from .hdf_read import * 
