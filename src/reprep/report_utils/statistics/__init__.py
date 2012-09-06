from .. import np, contract, logger
from .structures import *
from .data_view import *
from . import reductions

#    doc = f.__doc__
#    if doc is None:
#        logger.warning('No description for %s' % f)
#        doc = "(missing description)"
#    doc = doc.strip()
#    if ':=' in doc:
#        tokens = doc.split(':=')
#        symbol = tokens[0]
#        desc = "".join(tokens[1:])
#    else:
#        symbol = '\\text{%s}' % f.__name__  
#        desc = doc
#        
