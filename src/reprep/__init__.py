__version__ = "7.3"
__date__ = ""

from zuper_commons import ZLogger

logger = ZLogger(__name__)
logger.hello_module(name=__name__, filename=__file__, version=__version__, date=__date__)

from .config import *
from .constants import *
from .datanode import *
from .figure import *
from .graphics import *
from .interface import *
from .mpl import *
from .node import *
from .repcontracts import *
from .structures import *
from .table import *
from .types import *
from .utils import *


class Report(Node):
    pass


from . import report_utils  # just load demos

logger.hello_module_finished(__name__)
