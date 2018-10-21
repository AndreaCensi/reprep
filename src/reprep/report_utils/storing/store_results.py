# -*- coding: utf-8 -*-
from contracts import check_isinstance, contract, new_contract
from reprep.utils import deprecated, frozendict2, natsorted

__all__ = [
    'StoreResults',
]

class StoreResults(dict):
    
    def __getitem__(self, attrs):
        if not isinstance(attrs, frozendict2):
            check_isinstance(attrs, dict)
            attrs = frozendict2(**attrs)
        try:
            return dict.__getitem__(self, attrs)
        except KeyError as e:
            msg = str(e)
            keys = self.keys()
            if keys:
                k = most_similar(self.keys(), attrs)
                msg += '\n The most similar key is: %s' % str(k)
            raise KeyError(msg)
            
    
    def __setitem__(self, attrs, value):
        if not isinstance(attrs, dict):
            msg = 'Keys to this dictionary must be dicts'
            raise ValueError(msg)
        # Todo: check all strings
        frozen = frozendict2(**attrs)
        dict.__setitem__(self, frozen, value)

    def __contains__(self, attrs):
        frozen = frozendict2(**attrs)
        return dict.__contains__(self, frozen)

    def select(self, *cond, **condkeys):
        """ Returns another StoreResults with the filtered results. """
        # So that we can be subclassed with specialization 
        r = self.__class__() 
        for attrs in self.select_key(*cond, **condkeys):
            r[attrs] = self[attrs] 
        return r
    
    def remove_field(self, field):
        """ Returns a copy of this structure, where the given field
            is removed from the keys. Throws an error if removing the
            field would make the keys not unique. Also throws 
            an error if the given field is not present in all keys."""
        r = self.__class__() 
        for key in self:
            if not field in key:
                msg = "Could not find field %r in key %r." % (field, key)
                raise ValueError(msg)
            
            key2 = frozendict2(key)
            del key2[field]
            
            if key2 in r:
                msg = ('Removing field %r from key %r would make it non unique.' % 
                        (field, key))
                raise ValueError(msg)
            
            r[key2] = self[key] 
        return r

    def select_key(self, *conditions, **condkeys):
        """ 
            Selects keys according to some conditions, which could be either
            functions, or key=value queries.
        """
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

    @deprecated
    def field(self, field):
        """ Returns all values of the given field """
        return self.field_values(field)
    
    def field_values(self, field):
        """ Returns all values of the given field """
        for attrs in self:
            if not field in attrs:
                msg = 'Field %r not found in %s.' % (field, attrs)
                raise ValueError(msg)
            yield attrs[field]

    @contract(returns='list(str)')
    def field_names(self):
        """ 
            Returns all field names presents.
            Note that, in general, some fields might not be present in all entries.
        """
        if len(self) == 0:
            return []
        # XXX: check that all have the same ones
        names = set()
        for k in self:
            names.update(k.keys())
        return list(names)

    @contract(returns='list(str)')    
    def field_names_in_all_keys(self):
        """ 
            Returns the field names that are in all keys.
        """
        names = None
        for k in self:
            if names is  None:
                names = set(k.keys())
            else:
                names = names & set(k.keys())
            
        return list(names)
    
    @contract(returns='dict')
    def fields_with_unique_values(self):
        """ Returns a dictionary of fields which appear in all keys
            and that have the same value across all keys. """
        res = {}
        for field in self.field_names_in_all_keys():
            values = list(set(self.field_values(field)))
            if len(values) == 1:
                res[field] = values[0]
        return res
        
    
    def groups_by_field_value(self, field):
        """
            Partitions the contents according to the value of the given
            field.
            
            Example: :: 
            
                for delta, samples in x.groups_by_field_value('delta'):
                    ...
        """
        field_values = set(self.field(field))     
        # convert to string in order to sort
        sorted_values = natsorted(field_values)    
        for value in sorted_values:
            query = {field: value}
            samples = self.select(**query)
            assert samples
            assert field in samples.fields_with_unique_values()  # expensive

            yield value, samples
            
            
new_contract('StoreResults', StoreResults)        

        
             
     

def most_similar(keys, key):
    """ Returns the key which is most similar """

    def score(key1):
        v1 = set(key1.values())
        v2 = set(key.values())
        return len(v1 & v2)
    
    import numpy as np
    keys = list(keys)
    scores = np.array(map(score, keys))
    
#     tie = np.sum(scores == np.max(scores)) > 1
#     if tie:
#         # print('there is a tie: %s,\n %s' % (key, keys))
#         return None
#     
    best = keys[np.argmax(scores)]
    return best
    
    
         

