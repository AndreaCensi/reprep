from contracts import contract
from reprep.report_utils.statistics.structures import (Reduction,
    ReductionDisplay, RepRepStats)
from reprep.report_utils.store_results import StoreResultsDict
from reprep.report_utils.with_description import WithDescription

class DataView(WithDescription):
    """ This class defines how we view the data. """
    
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
        
    @contract(samples=StoreResultsDict, returns='tuple(*,*,*)')
    def reduce(self, samples):
        """
            Returns all stages: raw_data, reduction, display. 
        """
        field = self.source.get_name()
        data = list(samples.field_or_value_field(field))
        reduced = self.reduction.function(data)
        display = self.display.function(reduced)
        return data, reduced, display
    
    @staticmethod
    def from_string(s, source_fields={}):
        """ 
            Accepts the formats: 
            - source   =  source/all/string
            - source/reduction = source/reduction/string
            - source/reduction/display
        """
        tokens = s.split('/')
        if len(tokens) == 1:
            source = tokens[0]
            reduction = 'all'
            display = 'string'
        elif len(tokens) == 2:
            source = tokens[0]
            reduction = tokens[1]
            display = 'string'
        elif len(tokens) == 3:
            source = tokens[0]
            reduction = tokens[1]
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
    
