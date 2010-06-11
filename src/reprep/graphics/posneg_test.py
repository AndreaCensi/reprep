import unittest
from posneg import posneg
import numpy
from numpy  import nan


class Test(unittest.TestCase):

    valid_shapes = [(10, 10)]
    invalid_shapes = [(10,), (0, 10, 3), ()]
    
    def testValid(self):
        for shape in Test.valid_shapes:
            v = numpy.zeros(shape=shape, dtype='float32')
            v[...] = numpy.random.rand(*shape) * 255 
            posneg(v)


    def testInvalidShapes(self):
        for shape in Test.invalid_shapes:
            v = numpy.zeros(shape=shape, dtype='float32')
            self.assertRaises(ValueError, posneg, v)
            
    def testInvalidNumbers(self):
        a = numpy.ones(shape=(10, 10))
        a[0, 0] = nan
        self.assertRaises(ValueError, posneg, a)
            
