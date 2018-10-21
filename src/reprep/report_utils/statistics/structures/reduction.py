# -*- coding: utf-8 -*-
from .function_with_description import FunctionWithDescription

__all__ = [
    'Reduction',
]

class Reduction(FunctionWithDescription):
    def __init__(self, *args, **kwargs):
        super(Reduction, self).__init__(*args, **kwargs)
        
        if not "%s" in self.get_symbol():
            msg = ('Missing pattern for symbol of %r.' % self.get_name())
            raise ValueError(msg)
        
        if not "%s" in self.get_desc():
            msg = ('Missing pattern for desc of %r.' % self.get_name())
            raise ValueError(msg)
