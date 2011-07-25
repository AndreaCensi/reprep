from numpy import maximum, minimum, zeros
from . import contract, np

@contract(a='array', top_percent='>=0,<=90')
def skim_top(a, top_percent):
    ''' Cuts off the top percentile '''
    threshold = np.percentile(a.flat, 100 - top_percent) 
    return np.minimum(a, threshold)

  
@contract(value='array[HxW],H>0,W>0', max_value='None|number',
          skim='>=0,<=90', nan_color='color_spec')
def posneg(value, max_value=None, skim=0, nan_color=[0.5, 0.5, 0.5]):
    """ 
    Converts a 2D value to normalized uint8 RGB red=positive, blue=negative 0-255.
    
     
    """   
    value = value.astype('float32')
    value = value.squeeze().copy()
    
    isfinite = np.isfinite(value)
    isnan = np.logical_not(isfinite)
    # set nan to 0
    value[isnan] = 0
    
    if max_value is None:
        abs_value = abs(value)
        if skim != 0:
            abs_value = skim_top(abs_value, skim)
            
        max_value = np.max(abs_value)

    if max_value == 0:
        result = zeros((value.shape[0], value.shape[1], 3), dtype='uint8')
        return result

    assert np.isfinite(max_value)

    positive = minimum(maximum(value, 0), max_value) / max_value
    negative = maximum(minimum(value, 0), -max_value) / -max_value
    positive_part = (positive * 255).astype('uint8')
    negative_part = (negative * 255).astype('uint8')

    result = zeros((value.shape[0], value.shape[1], 3), dtype='uint8')
    
    anysign = maximum(positive_part, negative_part)
    R = 255 - negative_part[:, :]
    G = 255 - anysign
    B = 255 - positive_part[:, :]
    
    # remember the nans
    R[isnan] = nan_color[0] * 255
    G[isnan] = nan_color[1] * 255
    B[isnan] = nan_color[2] * 255
    
    result[:, :, 0] = R
    result[:, :, 1] = G
    result[:, :, 2] = B
    
    # TODO: colorbar
    
    return result
 
