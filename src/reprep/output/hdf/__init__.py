# -*- coding: utf-8 -*-
from ... import logger

def get_tables():
    import tables
    return tables

# try:
#     import tables
# except Exception as e:
#     logger.exception(e)
#     logger.warning('No HDF support. (%s)' % e)
#     raise

__all__ = ['to_hdf', 'report_from_hdf']
from .hdf1_rawdata import *
from .hdf1_read import *
from .hdf1_write import *
from .hdf_read import * 
