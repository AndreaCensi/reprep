import numpy, unittest
from numpy.linalg.linalg import pinv
from matplotlib import pylab

from reprep import Table, Node, Report

from .utils import ReprepTest

class Test(ReprepTest):    
    
    def testTable(self):
        
        table = Table('mytable',
                      [['Andrea', 'Censi'], ['a', 'b']], ['Name', 'Last'],
                      )
        self.node_serialization_ok(table)
    
    def testTable2(self):
        data = numpy.zeros((2, 2))
        table = Table('mytable', data)
        self.node_serialization_ok(table)
    
    def testTable3(self):
        dtype = numpy.dtype([('field1', 'int32'), ('field2', 'int32')])
        data = numpy.zeros(shape=(5,), dtype=dtype)
        table = Table('mytable', data)
        self.node_serialization_ok(table)
    
    def testTable4(self):
        data = numpy.zeros((2, 2, 3))
        self.assertRaises(ValueError, Table, 'mytable', data)
        
    def testTable5(self):
        dtype = numpy.dtype([('field1', 'int32'), ('field2', 'int32')])
        data = numpy.zeros(shape=(5, 4), dtype=dtype)
        self.assertRaises(ValueError, Table, 'mytable', data)

    
    def testImage(self):
        C = numpy.random.rand(50, 50)
        information = pinv(C)
        T = numpy.random.rand(50, 50, 3)
        
        report = Node('rangefinder')
        report.data('Tx', T[:, :, 0])
        report.data('Ty', T[:, :, 1])
        report.data('Tz', T[:, :, 2])
        cov = report.data('covariance', C)
        report.data('information', information)

        with cov.data_file('plot', 'image/png') as f:
            pylab.figure()
            pylab.plot(C)
            pylab.savefig(f)
            pylab.close()
                
        report.table('results',
                         cols=['One', 'Two'],
                         data=[[1, 2], [3, 4]])        
        
        f = report.figure('Covariance and information matrix', cols=3)
        f.sub('covariance', 'should default to plot')
        f.sub('covariance/plot', 'Same as <-')
            
        f = report.figure('Tensors', cols=3)
        f.sub('Tx', display='posneg')
        f.sub('Ty', display='posneg')
        f.sub('Tz', display='posneg')
        
        
        self.node_serialization_ok(report)

    def test_invalid_id(self):
        self.assertRaises(ValueError, Report, 1)

    def test_invalid_children(self):
        self.assertRaises(ValueError, Report, children=1)
        self.assertRaises(ValueError, Report, children=[1])
        self.assertRaises(ValueError, Report, children=[None])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
