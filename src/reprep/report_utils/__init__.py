from .. import logger, contract
import numpy as np

"""
    Some notes on how these classes are used together.
    
    StoreResults is a dictionary of  ::
    
        dict(key=value) -> Compmake Promise
    
    After computation, it will have some values: ::
    
        dict(key=value) -> dict(key2=value2,...)
        
    





"""


from .with_description import *

from .frozen import *
from .store_results import *
from .report_manager import *

from .statistics import *
from .tables import *
