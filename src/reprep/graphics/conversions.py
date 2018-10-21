# -*- coding: utf-8 -*-
from contracts import contract
import numpy as np


@contract(
    a='(array[HxW](uint8)|array[HxWx3](uint8)|array[HxWx4](uint8)),H>0,W>0')
def Image_from_array(a):
    ''' 
        Converts an image in a numpy array to an Image instance.
        Accepts:  h x w      255  interpreted as grayscale
        Accepts:  h x w x 3  255  RGB  
        Accepts:  h x w x 4  255  RGBA 
    '''

    if len(a.shape) == 2:
        height, width = a.shape
        rgba = np.zeros((height, width, 4), dtype='uint8')
        rgba[:, :, 0] = a
        rgba[:, :, 1] = a
        rgba[:, :, 2] = a
        rgba[:, :, 3] = 255
    elif len(a.shape) == 3:
        height, width = a.shape[0:2]
        depth = a.shape[2]
        rgba = np.zeros((height, width, 4), dtype='uint8')
        if not depth in [3, 4]:
            raise ValueError('Unexpected shape "%s".' % str(a.shape))
        rgba[:, :, 0:depth] = a[:, :, 0:depth]
        if depth == 3:
            rgba[:, :, 3] = 255
    else:
        assert False

    assert rgba.shape == (height, width, 4)

    from PIL import Image #@UnresolvedImport
    im = Image.frombuffer("RGBA", (width, height), rgba.data,  # @UndefinedVariable
                           "raw", "RGBA", 0, 1)
    return im
