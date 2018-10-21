# -*- coding: utf-8 -*-
from contracts import contract
from reprep.report_utils.storing.store_results import StoreResults
import numpy as np

__all__ = [
    'array_from_sr',           
]

@contract(sr=StoreResults, fields='seq(str)', returns='array')
def array_from_sr(sr, fields):
        
    if len(sr) == 0:
        raise ValueError('empty')
    
    order = list(sr)
    
    def get_values_for_field(field):
        values = []
        for s in order:
            v = sr[s]
            if field in s:
                values.append(s[field])
            elif field in v:
                values.append(v[field])
            else:
                msg = 'No field %r found in %r or %r' % (field, s, v)
                raise ValueError(msg)
        return values
    
    dtype = []    
    for f in fields:
        values = get_values_for_field(f)
        assert len(values) == len(sr)
        a = np.array(values[0])
        dt = (a.dtype, a.shape)
        dtype.append((f, dt))
    dtype = np.dtype(dtype)
    a = np.ndarray(dtype=dtype, shape=len(sr))
    for f in fields:
        values = get_values_for_field(f)
        for i in range(len(values)):
            a[i][f] = values[i]
    return a

