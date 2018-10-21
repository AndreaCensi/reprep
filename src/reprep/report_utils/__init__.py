# -*- coding: utf-8 -*-
"""
    Some notes on how these classes are used together.
    
    StoreResults is a dictionary of  ::
    
        dict(key=value) -> Compmake Promise
    
    After computation, it will have some values: ::
    
        dict(key=value) -> dict(key2=value2,...)
        
"""

from .storing import *
from .statistics import *

