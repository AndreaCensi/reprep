import numpy
import Image

from .numpy_utils import gt, require_shape, require_array

def Image_from_array(a):
    ''' Converts an image in a numpy array to an Image instance.
        Accepts:  h x w      255  interpreted as grayscale
        Accepts:  h x w x 3  255  rgb  
        Accepts:  h x w x 4  255  rgba '''
        
    require_array(a)

    if not a.dtype == 'uint8':
        raise ValueError('I expect dtype to be uint8, got "%s".' % a.dtype)
    
    if len(a.shape) == 2:
        height, width = a.shape
        rgba = numpy.zeros((height, width, 4), dtype='uint8')
        rgba[:, :, 0] = a
        rgba[:, :, 1] = a
        rgba[:, :, 2] = a
        rgba[:, :, 3] = 255
    elif len(a.shape) == 3:
        height, width = a.shape[0:2]
        depth = a.shape[2]
        rgba = numpy.zeros((height, width, 4), dtype='uint8')
        if not depth in [3, 4]:
            raise ValueError('Unexpected shape "%s".' % str(a.shape))
        rgba[:, :, 0:depth] = a[:, :, 0:depth]
        if depth == 3:
            rgba[:, :, 3] = 255
    else:
        raise ValueError('Unexpected shape "%s".' % str(a.shape))
    
    require_shape((gt(0), gt(0), 4), rgba) 
    
    
    im = Image.frombuffer("RGBA", (width, height), rgba.data,
                           "raw", "RGBA", 0, 1)
    return im
