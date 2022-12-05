"""
    Some notes on how these classes are used together.

    StoreResults is a dictionary of  ::

        dict(key=value) -> Compmake Promise

    After computation, it will have some values: ::

        dict(key=value) -> dict(key2=value2,...)

"""
from .. import logger

logger.hello_module(name=__name__, filename=__file__, version="n/a", date="n/a")

from .storing import *
from .statistics import *

logger.hello_module_finished(__name__)
