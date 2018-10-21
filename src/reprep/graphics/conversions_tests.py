# -*- coding: utf-8 -*-
from . import Image_from_array, np
import unittest


class Test(unittest.TestCase):

    valid_shapes = [(10, 10), (10, 10, 3), (10, 10, 4)]
    invalid_shapes = [(10, 0), (0, 10, 3), (10, 0, 4), (10, 10, 5), (), (10)]

    def testValid(self):
        for shape in Test.valid_shapes:
            v = np.zeros(shape=shape, dtype='uint8')
            v[...] = np.random.rand(*shape) * 255
            Image_from_array(v)

    def testInvalidShapes(self):
        for shape in Test.invalid_shapes:
            v = np.zeros(shape=shape, dtype='uint8')
            print('Trying with %s' % str(v.shape))
            self.assertRaises(Exception, Image_from_array, v)

