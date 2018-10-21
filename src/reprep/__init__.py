# -*- coding: utf-8 -*-
__version__ = '2.11.0'

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


from contracts import contract, new_contract, describe_value, describe_type
import numpy as np

from .mpl import *
from .structures import *
from .constants import *
from .repcontracts import *
from .config import *
from .utils import *
from .interface import *
from .graphics import *
from .node import *
from .datanode import *
from .figure import *
from .table import *

# Alias
Report = Node


from . import report_utils # just load demos
