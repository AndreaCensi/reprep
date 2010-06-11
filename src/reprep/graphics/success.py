import numpy
from reprep.graphics.numpy_utils import gt, require_shape, require_array, \
    assert_finite

def colormap_rgba(values, colors, invalid_color=[255, 255, 0, 255],
                   nan_color=[0, 0, 0, 0]):
    ''' entries = [ (min, max, [r,g,b,a]),... ] '''
    require_shape((gt(0), gt(0)), values)
    h, w = values.shape
    res = numpy.zeros(shape=(h, w, 4), dtype='uint8')
    for i in range(h):
        for j in range(w):
            chosen = invalid_color
            val = values[i, j]
            for vmin, vmax, color in colors:
                if vmin <= val <= vmax:
                    chosen = color
                    break
            if numpy.isnan(val):
                chosen = nan_color
            res[i, j, :] = chosen
    return res


def colorize_success(value):
    require_array(value)
    assert_finite(value)
    if value.max() > 1 or value.min() < 0:
        raise ValueError('I expect a probability matrix.')
    
    red = [255, 0, 0, 255]
    magenta = [186, 50, 50, 255]
    yellow = [255, 255, 0, 255]
    orange = [255, 164, 18, 255]
    blue = [0, 0, 255, 255]
    bluegreen = [255, 255, 120, 255]
    darkgreen = [0, 100, 0 , 255]
    green = [0, 255, 0, 255]
    
    colors = [(0, 0.001, red), (0.001, 0.05, magenta), (0.05, 0.25, yellow),
              (0.25, 0.50, orange), (0.5, 0.75, blue), (0.75, 0.95, bluegreen),
              (0.95, 0.99, darkgreen), (0.99, 1, green) ]
    rgba = colormap_rgba(value, colors)
    return rgba
