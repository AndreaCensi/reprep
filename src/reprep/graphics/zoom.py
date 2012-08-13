from . import contract, np


@contract(M='array[HxWx3](uint8)', K='K,>=1',
          returns='array[(H*K)x(W*K)x3](uint8)')
def rgb_zoom(M, K=10):
    ''' Zooms an RGB image by a fixed factor. '''
    if K == 1:
        return M.copy()
    H, W, _ = M.shape
    Z = np.zeros((H * K, W * K, 3), 'uint8')
    for i in range(3):
        Z[:, :, i] = np.kron(M[:, :, i], np.ones((K, K)))
    return Z
