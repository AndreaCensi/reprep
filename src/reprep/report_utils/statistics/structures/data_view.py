# -*- coding: utf-8 -*-
from .reduction import Reduction
from .reduction_display import ReductionDisplay
from .storage import RepRepStats
from .with_description import WithDescription
from contracts import contract, new_contract
from reprep.report_utils.storing import StoreResultsDict

__all__ = [
    'DataView',
]

class DataView(WithDescription):
    """ This class defines how we view the data. """
    NOT_AVAILABLE = 'n/a'
    
    @contract(source=WithDescription, reduction=Reduction, display=ReductionDisplay)
    def __init__(self, source, reduction, display, *args, **kwargs):
        '''        
        :param name: ID for this view
        :param source: the source field in the data
        :param reduce: the reduction function (one defined in RepRepStats)
        :param display: the display function (from number to string) (one defined in RepRepStats)
        :param symbol: A LaTeX expression.
        :param desc: A free-form string.
        '''
        super(DataView, self).__init__(*args, **kwargs)
        self.source = source
        self.reduction = reduction
        self.display = display
        
    def __repr__(self):
        return 'DataView(%r,%r,%r)' % (self.source, self.reduction, self.display)
     
    @contract(samples=StoreResultsDict, returns='tuple(*,*,*)')
    def reduce(self, samples):
        """
            Returns all stages: raw_data, reduction, display. 
        """
        field = self.source.get_name()
        data = list(samples.field_or_value_field(field))
        reduced = self.reduction.function(data)
        if reduced is None:
            display = DataView.NOT_AVAILABLE
        else:
            display = self.display.function(reduced)
        return data, reduced, display
    
    @staticmethod
    def from_string(s, source_fields={}):
        """ 
            Accepts the formats: 
            - source   =  source/one/string
            - source/reduction = source/reduction/string
            - source/reduction/display
            - source//display => source/one/display
        """
        tokens = s.split('/')
        if len(tokens) == 1:
            source = tokens[0]
            reduction = 'one'
            display = 'string'
        elif len(tokens) == 2:
            source = tokens[0]
            reduction = tokens[1]
            if len(reduction) == 0:
                reduction = 'one'
            display = 'string'
        elif len(tokens) == 3:
            source = tokens[0]
            reduction = tokens[1]
            if len(reduction) == 0:
                reduction = 'one'
            display = tokens[2]
        else:
            msg = 'Wrong format %r' % s
            raise ValueError(msg)
    
        name = '%s_%s' % (source, reduction)    
    
        source = source_fields[source]
        reduction = RepRepStats.get_reduction(reduction)
        display = RepRepStats.get_display(display)

        symbol = reduction.get_symbol() % source.get_symbol()
    
        sdesc = source.get_desc()
        if sdesc:
            sdesc = sdesc[0].lower() + sdesc[1:] 
        desc = reduction.get_desc() % sdesc
          
        return DataView(name=name, source=source,
                        reduction=reduction, display=display,
                        desc=desc, symbol=symbol)
    
new_contract('DataView', DataView)
