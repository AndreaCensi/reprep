
version = '1.0'
__version__ = version

from contracts import contract, new_contract, describe_value, describe_type
import numpy as np

# XXX only import things explicitely
from .constants import *
from .utils import *
from .interface import *
from .graphics import *
from .node import *
from .figure import *

from .table import *

# Alias
Report = Node


