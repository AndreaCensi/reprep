# -*- coding: utf-8 -*-
from contracts import contract
import numpy as np

__all__ = ['rgb_zoom']

@contract(M='array[HxWx(C,(3|4))](uint8)', K='K,>=1',
          returns='array[(H*K)x(W*K)xC](uint8)')
def rgb_zoom(M, K=10):
    ''' Zooms an RGB image by a fixed factor. '''
    if K == 1:
        return M.copy()
    H, W, C = M.shape
    Z = np.zeros((H * K, W * K, C), 'uint8')
    for i in range(C):
        Z[:, :, i] = np.kron(M[:, :, i], np.ones((K, K)))
    return Z
