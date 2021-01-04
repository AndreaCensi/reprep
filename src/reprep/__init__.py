__version__ = "7.1.2101042139"
__date__ = "2021-01-04T21:39:18.852403"

from zuper_commons import ZLogger

logger = ZLogger(__name__)
logger.hello_module(
    name=__name__, filename=__file__, version=__version__, date=__date__
)

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
