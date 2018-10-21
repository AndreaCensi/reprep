# -*- coding: utf-8 -*-
from contracts import describe_type, new_contract
from reprep.report_utils.storing.store_results import StoreResults

__all__ = [
    'StoreResultsDict',
]

class StoreResultsDict(StoreResults):
    """ 
        This class is a StoreResults that assumes that also 
        the values are dictionaries. 
    """

    def __setitem__(self, attrs, value):
        if not isinstance(value, dict):
            msg = ('Values to this dictionary must be dicts; found %s' % 
                   describe_type(value))
            raise ValueError(msg)
        for k in attrs:
            if k in value:
                msg = ('The same field %r is found in both key and value. \n'
                       '  key: %s \n' 
                       'value: %s' % (k, attrs, value))
                raise ValueError(msg)
        super(StoreResultsDict, self).__setitem__(attrs, value)
    
    def field_or_value_field(self, field):
        """ 
            Returns all values for field, which can be either in the 
            key or in the value dict.
        """
        for k, v in self.items():
            if field in k:
                yield k[field]
            elif field in v:
                yield v[field]
            else:
                msg = ('Could not find value of %r neither in key or value. '
                       'Key: %s Value: %s' % 
                       (field, k, v))
                raise ValueError(msg)
            
            
    
    
new_contract('StoreResultsDict', StoreResultsDict)


