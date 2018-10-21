# -*- coding: utf-8 -*-
from reprep import  filter_colormap
import numpy as np


def get_test_bar(shape=(100, 10), M=10, dtype='float32', with_strange=False):
    bar = np.vstack([np.linspace(-M * 1.1, M * 1.2, shape[0])] * shape[1]).T
    bar = bar.astype(dtype)
    if with_strange:
        pos = bar > M
        nan = bar > M * 1.1
        neg = bar < -M
        bar[pos] = +np.Inf
        bar[neg] = -np.Inf
        bar[nan] = np.NaN
    return bar


def get_examples():
    ''' 
        Returns some examples of things that can be passed to 
        filter_colormap. 
    '''
    yield get_test_bar(dtype='int', with_strange=False)
    yield get_test_bar(dtype='uint8', with_strange=False)
    yield get_test_bar(dtype='int8', with_strange=False)
    yield get_test_bar(dtype='float32', with_strange=True)
    yield get_test_bar(dtype='float64', with_strange=True)
    yield np.zeros((10, 10), dtype='float32')
    yield np.zeros((10, 10), dtype='float64')
    yield np.zeros((10, 10), dtype='int')
    yield np.zeros((10, 10), dtype='int8')
    yield np.zeros((10, 10), dtype='uint8')


def test_filter_colormaps():
    cmap = 'Accent'

    for example in get_examples():
        properties = {}
        _ = filter_colormap(example, cmap=cmap, properties=properties)
        properties['nan_color']
        properties['inf_color']
        properties['flat_color']


