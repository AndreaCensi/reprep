from .. import logger, contract
import numpy as np

"""
    Some notes on how these classes are used together.
    
    StoreResults is a dictionary of  ::
    
        dict(key=value) -> Compmake Promise
    
    After computation, it will have some values: ::
    
        dict(key=value) -> dict(key2=value2,...)
        
    





"""

from .storing import *
from .repmanager import *
from .statistics import *

