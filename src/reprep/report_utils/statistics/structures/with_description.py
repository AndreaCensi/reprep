# -*- coding: utf-8 -*-
from reprep import logger
from contracts import new_contract


__all__ = [
    'WithDescription',
]

class WithDescription(object):
    """ Descriptive fields for objects """
    
    def __init__(self, name, desc=None, symbol=None):
        self._name = name
        self._desc = desc
        self._symbol = symbol

    def __repr__(self):
        return '%s(name=%r)' % (self.__class__.__name__,
                                 self._name)

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
        
new_contract('WithDescription', WithDescription)

