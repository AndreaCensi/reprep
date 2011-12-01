from . import contract, np, skim_top
from numpy import maximum, minimum, zeros


  
@contract(value='array[HxW],H>0,W>0', max_value='None|number',
          skim='>=0,<=90', nan_color='color_spec')
def posneg(value, max_value=None, skim=0, nan_color=[0.5, 0.5, 0.5],
           properties=None):
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
        # In this case, it means that all is 0
        max_value = 1 # don't divide by 0 later
        
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
    if properties is not None:
        properties['min_value'] = -max_value
        properties['max_value'] = max_value
        properties['nan_color'] = nan_color
        bar_shape = (512, 128)
        bar = np.vstack([np.linspace(-1, 1, bar_shape[0])] * bar_shape[1]).T
        properties['color_bar'] = posneg(bar)
        
        
    return result
 
