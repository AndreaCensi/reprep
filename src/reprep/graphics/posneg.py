import numpy
from numpy import maximum, minimum, zeros
from reprep.graphics.numpy_utils import assert_finite, gt, require_shape


def posneg(value, max_value=None):
    """ Converts a 2D value to normalized uint8 RGB red=positive, blue=negative 0-255
     
    """
    assert_finite(value)
    value = value.squeeze()
    require_shape((gt(0), gt(0)), value)
    
    if max_value is None:
        max_value = numpy.max(abs(value))
        if max_value == 0:
            raise ValueError('You asked to normalize a matrix which is all 0')

    positive_part = abs((maximum(value, 0) / max_value) * 255).astype('uint8')
    negative_part = abs((minimum(value, 0) / max_value) * 255).astype('uint8')
    result = zeros((value.shape[0], value.shape[1], 3), dtype='uint8')
    
    anysign = maximum(positive_part, negative_part)
    result[:, :, 0] = 255 - negative_part[:, :]
    result[:, :, 1] = 255 - anysign
    result[:, :, 2] = 255 - positive_part[:, :]
    
    return result
 
 
