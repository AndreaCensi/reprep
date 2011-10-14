
version = '1.0'
__version__ = version

from contracts import contract


# XXX only import things explicitely
from .constants import *
from .utils import *
from .figure import *
from .graphics import posneg, scale
from .interface import *
from .node import *
from .table import *

# Alias
Report = Node


