import numpy
from numpy import maximum, minimum, zeros
from reprep.graphics.numpy_utils import assert_finite, gt, require_shape
from reprep.graphics.posneg import skim_top


def scale(value, min_value=None, max_value=None,
                 min_color=[1, 1, 1], max_color=[0, 0, 0], skim=0):
    """ Provides a RGB representation of the values by interpolating the range 
        [min(value),max(value)] into the colorspace [min_color, max_color].
    
    Args:
      value:      a numpy array with finite values squeeze()able to (W,H).
      min_value:  If specified, this is taken to be the threshold. Everything
                  below min_value is considered to be equal to min_value.
      max_value:  Optional upper threshold.
      min_color:  color associated to minimum value. Default: [1,1,1] = white.
      max_color:  color associated to maximum value. Default: [0,0,0] = black.
    
    Returns:  a (W,H,3) numpy array with dtype uint8 representing a RGB image.
      
    """
    assert_finite(value)
    value = value.squeeze()
    require_shape((gt(0), gt(0)), value)
    
    min_color = numpy.array(min_color)
    max_color = numpy.array(max_color)
    require_shape((3,), min_color)
    require_shape((3,), max_color)
    
    if skim != 0:
        value = skim_top(value, skim)

    if max_value is None:
        max_value = numpy.max(value)
            
       
    if min_value is None:
        min_value = numpy.min(value)

    if max_value == min_value:
        result = zeros((value.shape[0], value.shape[1], 3), dtype='uint8')
        return result
        #raise ValueError('I end up with max_value = %s = %s = min_value.' % \
        #                 (max_value, min_value))

    value01 = (value - min_value) / (max_value - min_value)
    
    # Cut at the thresholds
    value01 = maximum(value01, 0)
    value01 = minimum(value01, 1)

    result = zeros((value.shape[0], value.shape[1], 3), dtype='uint8')
    
    for u in [0, 1, 2]:
        result[:, :, u] = 255 * ((1 - value01) * min_color[u] \
                                 + (value01) * max_color[u])
    
    return result
 
