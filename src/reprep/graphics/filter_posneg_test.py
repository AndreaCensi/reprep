# -*- coding: utf-8 -*-
from . import posneg, np
import unittest


class Test(unittest.TestCase):

    valid_shapes = [(10, 10)]
    invalid_shapes = [(10,), (0, 10, 3), ()]

    def testValid(self):
        for shape in Test.valid_shapes:
            v = np.zeros(shape=shape, dtype='float32')
            v[...] = np.random.rand(*shape) * 255
            posneg(v)

    def testInvalidShapes(self):
        for shape in Test.invalid_shapes:
            v = np.zeros(shape=shape, dtype='float32')
            self.assertRaises(Exception, posneg, v)

    def testInvalidNumbers(self):
        pass
        # we now have nan support in posneg
        # a = np.ones(shape=(10, 10))
        # a[0, 0] = nan
        # self.assertRaises(ValueError, posneg, a)

# TODO: add RGB(a) mcdp_lang_tests
