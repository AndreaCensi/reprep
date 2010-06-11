import unittest

from reprep import Table, Node
import numpy
import pylab
from reprep.out.html import node_to_html_document
from numpy.linalg.linalg import pinv

class Test(unittest.TestCase):

    def tryWritingOutput(self, node):
        node_to_html_document(node, 'tests/%s.html' % node.id)
    
    
    def testTable(self):
        
        table = Table('mytable',
                      [['Andrea', 'Censi'], ['a', 'b']], ['Name', 'Last'],
                      ['Developer', 'User'])
        self.tryWritingOutput(table)
        
    def testImage(self):
        C = numpy.random.rand(50, 50)
        information = pinv(C)
        T = numpy.random.rand(50, 50, 3)
        
        report = Node('rangefinder')
        report.data('Tx', T[:, :, 0])
        report.data('Ty', T[:, :, 1])
        report.data('Tz', T[:, :, 2])
        cov = report.data('covariance', C, desc="Covariance matrix")
        inf = report.data('information', information)

        with cov.data_file('plot', 'image/png') as f:
            pylab.figure()
            pylab.plot(C)
            pylab.close()
            pylab.savefig(f)
                
        t = report.table('results',
                         col_desc=['One', 'Two'],
                         data=[[1, 2], [3, 4]])        
        
        f = report.figure('Covariance and information matrix', shape=(1, 3))
        f.sub('covariance')
        f.sub('covariance/plot')
        f.sub('information')
            
        f = report.figure('Tensors', shape=(1, 3))
        f.sub('Tx', display='posneg')
        f.sub('Ty', display='posneg')
        f.sub('Tz', display='posneg')
        
        
        self.tryWritingOutput(report)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
