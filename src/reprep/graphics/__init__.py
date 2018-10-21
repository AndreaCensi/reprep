# -*- coding: utf-8 -*-
from .. import np, new_contract, contract
new_contract('color_spec', 'seq[3](>=0,<=1)')

from .conversions import Image_from_array
from .success import colorize_success
from .scaling import *
from .filter_colormap import *
from .filter_posneg import posneg
from .filter_scale import scale
from .zoom import *
