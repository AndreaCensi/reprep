from . import logger
from contracts import contract

class WithDescription(object):
    """ Descriptive fields for objects """
    
    def __init__(self, name, desc=None, symbol=None):
        self._name = name
        self._desc = desc
        self._symbol = symbol

    def get_name(self):
        return self._name
    
    def get_symbol(self):
        if self._symbol is None:
            logger.warning('No symbol for %r.' % self._name)
            return '\\text{%s}' % self._name
        else:
            return self._symbol
        
    def get_desc(self):
        if self._desc is None:
            logger.warning('No desc for %r.' % self._name)
            return '(Missing desc for %r)' % self._name
        else:
            if '\n' in self._desc:
                logger.warning('Description with newlines for %r.' % self._name)
                logger.warning(self._desc)
            return self._desc
        

@contract(returns='tuple(str,str)')
def symbol_desc_from_docstring(f):
    doc = f.__doc__
    if doc is None:
        logger.warning('No docstring for %s' % f)
        symbol, desc = None, None
    else:
        symbol, desc = symbol_desc_from_string(doc)
#    if symbol is None:
#        logger.warning('No symbol for %s' % f)
#        symbol = '\\text{%s}' % f.__name__  
#    
    return symbol, desc
    
    
@contract(returns='tuple(str,str)')
def symbol_desc_from_string(doc):
    """ Expects something like: ::
    
            M := Number of edges.
            
            blah blah
    
        Gets only the first line of the description. """
    doc = doc.strip()
    if ':=' in doc:
        tokens = doc.split(':=')
        symbol = tokens[0]
        #desc = "".join(tokens[1:])
        rest = tokens[1]
        lines = rest.split('\n')
        desc = lines[0]
    else:
        symbol = None
        lines = doc.split('\n')
        desc = lines[0]
        
    assert not '\n' in desc
    return symbol, desc
        

class FunctionWithDescription(WithDescription):
    """ A function with a description """

    def __init__(self, function, *args, **kwargs):
        super(FunctionWithDescription, self).__init__(*args, **kwargs)
        self.function = function
