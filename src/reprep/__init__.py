__version__ = '2.1'

from PIL import Image #@UnresolvedImport

from contracts import contract, new_contract, describe_value, describe_type
import numpy as np


import logging
logging.basicConfig()

logger = logging.getLogger(__name__)

from .mpl import *

# XXX only import things explicitely
from .structures import *
from .constants import *
from .repcontracts import *
from .config import *
from .utils import *
from .interface import *
from .graphics import *
from .node import *
from .figure import *
from .table import *

# Alias
Report = Node


