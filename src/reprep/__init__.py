# -*- coding: utf-8 -*-
__version__ = "6.0.3"

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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

from .types import *

# Alias
Report = Node


from . import report_utils  # just load demos
