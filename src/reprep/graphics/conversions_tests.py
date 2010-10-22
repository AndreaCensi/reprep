import unittest
import numpy
from reprep.graphics.conversions import Image_from_array


class Test(unittest.TestCase):

    valid_shapes = [(10, 10), (10, 10, 3), (10, 10, 4)]
    invalid_shapes = [(10, 0), (0, 10, 3), (10, 0, 4), (10, 10, 5), (), (10)]
    
    def testValid(self):
        for shape in Test.valid_shapes:
            v = numpy.zeros(shape=shape, dtype='uint8')
            v[...] = numpy.random.rand(*shape) * 255 
            Image_from_array(v)


    def testInvalidShapes(self):
        for shape in Test.invalid_shapes:
            v = numpy.zeros(shape=shape, dtype='uint8')
            self.assertRaises(ValueError, Image_from_array, v)
            
