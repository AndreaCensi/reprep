from numpy import isnan, isinf, isfinite
import numpy

class gt:
    def __init__(self, n):
        self.n = n
    def __eq__(self, other):
        return other > self.n
    
    def __str__(self):
        return '>%s' % self.n 

class square_shape:
    def __eq__(self, other):
        return len(other) == 2  and other[0] == other[1] 

def require_shape(expected_shape, v):
    require_array(v)
    if not expected_shape == v.shape:
        raise ValueError('Expecting shape %s, got %s' % 
                         (expected_shape, v.shape))  

def require_array(v):
    if not isinstance(v, numpy.ndarray):
        raise ValueError('Expecting a numpy array, got %s.' % 
                         str(type(v)))

    
def assert_finite(a):
    require_array(a)
    if not isfinite(a).all():
        raise ValueError('Invalid value %s' % a)
