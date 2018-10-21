# -*- coding: utf-8 -*-
from contracts import contract
from reprep import logger

@contract(returns='tuple(None|str,None|str)')
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
    
    
@contract(returns='tuple(None|str,str)')
def symbol_desc_from_string(doc):
    """ Expects something like: ::
    
            M := Number of edges.
            
            blah blah
    
        Gets only the first line of the description. """
    doc = doc.strip()
    if ':=' in doc:
        tokens = doc.split(':=')
        symbol = tokens[0]
        # desc = "".join(tokens[1:])
        rest = tokens[1]
        lines = rest.split('\n')
        desc = lines[0]
    else:
        symbol = None
        lines = doc.split('\n')
        desc = lines[0]
        
    assert not '\n' in desc
    return symbol, desc
        
