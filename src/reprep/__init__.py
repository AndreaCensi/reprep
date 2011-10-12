
version = '1.0'
__version__ = version

# XXX only import things explicitely
from .figure import *
from .graphics import posneg, scale
from .interface import *
from .node import *
from .table import *

# Alias
Report = Node


