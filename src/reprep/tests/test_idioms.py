# -*- coding: utf-8 -*-
from .common import ReprepTest
from contracts import ContractNotRespected
from numpy.linalg.linalg import pinv
from reprep import (MIME_PLAIN, Table, Node, Report)
import numpy
import unittest
from reprep.mpl import get_pylab_instance


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

    def testImageRGB(self):
        rgb = numpy.zeros((4, 4, 3), 'uint8')
        report = Node('test')
        report.data_rgb('rgb', rgb)

    def testImageRGBCaption(self):
        rgb = numpy.zeros((4, 4, 3), 'uint8')
        r = Report('test')
        r.data_rgb('rgb', rgb, caption='ciao')

    def testFigures(self):
        rgb = numpy.zeros((4, 4, 3), 'uint8')
        r = Report('test')
        f = r.figure()
        f.data_rgb('rgb', rgb, caption='ciao')
        assert len(f.get_subfigures()) == 1
        r.data_rgb('rgb', rgb, caption='ciao2')
        r.last().add_to(f)
        assert len(f.get_subfigures()) == 2

    def testPlot(self):
        r = Report('test')
        with r.plot('ciao') as pylab:
            pylab.plot([0, 1], [0, 1], '-k')

    def testPlotCaption(self):
        r = Report('test')
        with r.plot('ciao', caption='my caption') as pylab:
            pylab.plot([0, 1], [0, 1], '-k')

    def testText(self):
        r = Report('test')
        r.text('ciao', 'come va?')

    def testText2(self):
        r = Report('test')
        r.text('ciao', 'come va?', MIME_PLAIN)

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

        pylab = get_pylab_instance()
        with cov.data_file('plot', 'image/png') as f:
            pylab.figure()
            pylab.plot(C)
            pylab.savefig(f)
            pylab.close()

        report.table('results',
                         cols=['One', 'Two'],
                         data=[[1, 2], [3, 4]])

        f = report.figure(caption='Covariance and information matrix', cols=3)
        f.sub('covariance', 'should default to plot')
        f.sub('covariance/plot', 'Same as <-')

        f = report.figure('Tensors', cols=3)
        f.sub('Tx', display='posneg')
        f.sub('Ty', display='posneg')
        f.sub('Tz', display='posneg')

        self.node_serialization_ok(report)

    def test_invalid_id(self):
        self.assertRaises((ValueError, ContractNotRespected), Report, 1)

    def test_invalid_id_2(self):
        valid = [
            'cioa',
            'cioa',
            'cioa_',
            'cioa-0.4',
            'cioa-',
        ]
        invalid = [
             'cioa/',
             'cioa:',
             'cioa ',
             'cioa <',
             '$cioa',
             ' cioa',
             '',
             '"',
             '""',
             "'",
             "a\\a",
        ]
        for s in invalid:
            print('TRying with %r' % s)
            self.assertRaises((ValueError, ContractNotRespected), Report, s)

        for s in valid:
            Report(s)

    def test_invalid_children(self):
        self.assertRaises((ValueError, ContractNotRespected),
                          Report, children=1)
        self.assertRaises((ValueError, ContractNotRespected),
                          Report, children=[1])
        self.assertRaises((ValueError, ContractNotRespected),
                          Report, children=[None])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
