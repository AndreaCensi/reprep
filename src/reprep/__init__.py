
version = '1.1'
__version__ = version


import matplotlib
if matplotlib.get_backend() != 'agg':
    matplotlib.use('agg')
from matplotlib import pylab as reprep_pylab_instance

from contracts import contract, new_contract, describe_value, describe_type
import numpy as np

# XXX only import things explicitely
from .structures import *
from .constants import *
from .utils import *
from .interface import *
from .graphics import *
from .node import *
from .figure import *
from .table import *

# Alias
Report = Node


