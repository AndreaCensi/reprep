__version__ = "7.3"
__date__ = ""

from typing_extensions import TypeAlias

from zuper_commons import ZLogger

logger = ZLogger(__name__)
logger.hello_module(name=__name__, filename=__file__, version=__version__, date=__date__)

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


class Report(Node):
    pass


from . import report_utils  # just load demos

logger.hello_module_finished(__name__)
