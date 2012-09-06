
from reprep.report_utils.with_description import (
    FunctionWithDescription, symbol_desc_from_docstring)

        
class Reduction(FunctionWithDescription):
    def __init__(self, *args, **kwargs):
        super(Reduction, self).__init__(*args, **kwargs)
        
        if not "%s" in self.get_symbol():
            msg = ('Missing pattern for symbol of %r.' % self.get_name())
            raise ValueError(msg)
        
        if not "%s" in self.get_desc():
            msg = ('Missing pattern for desc of %r.' % self.get_name())
            raise ValueError(msg)
        

class ReductionDisplay(FunctionWithDescription):
    pass

        
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
