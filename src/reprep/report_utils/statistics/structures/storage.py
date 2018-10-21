# -*- coding: utf-8 -*-
from .reduction import Reduction
from .reduction_display import ReductionDisplay
from .with_description_utils import symbol_desc_from_docstring

__all__ = [
    'RepRepStats',
]
        
class RepRepStats(object):
    reductions = {}
    display = {}

    @staticmethod
    def reduction(f):
        """ Add as a reduction function. """
        name = f.__name__
        symbol, desc = symbol_desc_from_docstring(f)
        assert not '\n' in desc, desc
        red = Reduction(name=name, function=f, desc=desc, symbol=symbol)
        RepRepStats.reductions[name] = red
        return f

    @staticmethod
    def get_reduction(name):
        return RepRepStats.reductions[name]
    
    @staticmethod
    def reduction_display(f):
        """ Add as a reduction display function. """
        name = f.__name__
        desc = f.__doc__
        if desc is None:
            desc = ""
        symbol = ""
        red = ReductionDisplay(name=name, function=f, desc=desc, symbol=symbol)
        RepRepStats.display[name] = red
        return f

    @staticmethod
    def get_display(name):
        return RepRepStats.display[name]
