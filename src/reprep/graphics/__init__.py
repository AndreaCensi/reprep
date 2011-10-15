from .. import np, new_contract, contract
new_contract('color_spec', 'seq[3](>=0,<=1)')

from .conversions import Image_from_array
from .success import colorize_success
from .filter_posneg import posneg, skim_top
from .filter_scale import scale
