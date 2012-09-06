from contracts.interface import describe_type
from reprep.report_utils import frozendict2
from reprep.utils import natsorted
from contracts import new_contract

frozendict = frozendict2

class StoreResults(dict):
    
    def __setitem__(self, attrs, value):
        if not isinstance(attrs, dict):
            msg = 'Keys to this dictionary must be dicts'
            raise ValueError(msg)
        dict.__setitem__(self, frozendict(**attrs), value)

    def select(self, *cond, **condkeys):
        """ Returns another StoreResults with the filtered results. """
        # So that we can be subclassed with specialization 
        r = self.__class__() 
        for attrs in self.select_key(*cond, **condkeys):
            r[attrs] = self[attrs] 
        return r

    def select_key(self, *conditions, **condkeys):
        for attrs in self:
            for c in conditions:
                if not c(attrs):
                    break
            else:
                for k in condkeys:
                    if condkeys[k] != attrs[k]:
                        break
                else:
                    yield attrs

    def field(self, field):
        """ Returns all values of the given field """
        for attrs in self:
            if not field in attrs:
                msg = 'Field %r not found in %s.' % (field, attrs)
                raise ValueError(msg)
            yield attrs[field]

    def field_names(self):
        """ Returns all field names """
        if len(self) == 0:
            return []
        # XXX: check that all have the same ones
        for k in self:
            return list(k.keys())
        
    def groups_by_field_value(self, field):
        """
            Partitions the contents according to the value of the given
            field.
            
            Example: :: 
            
                for delta, samples in x.groups_by_field_values('delta'):
                    ...
        """
        field_values = set(self.field(field))     
        # convert to string in order to sort
        sorted_values = natsorted(field_values)    
        for value in sorted_values:
            query = {field: value}
            samples = self.select(**query)
            assert samples
            yield value, samples
            
class StoreResultsDict(StoreResults):
    """ This class assumes that also the values are dictionaries. """
    
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
                
            
new_contract('StoreResults', StoreResults)        
new_contract('StoreResultsDict', StoreResultsDict)
        
            
            
            
    
     
         

