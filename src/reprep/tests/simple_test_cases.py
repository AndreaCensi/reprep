# -*- coding: utf-8 -*-
import numpy as np
from reprep.tests.cases import ExampleReports
from reprep import MIME_PLAIN, Table


@ExampleReports.add
def raw_integer(r):
    r.data('integer', 1)
    
@ExampleReports.add
def raw_float(r):
    r.data('float', 1.0)

@ExampleReports.add
def raw_string(r):
    r.data('string', "ciao")
    
@ExampleReports.add
def raw_dict(r):
    r.data('dict', dict(a=1))
    


@ExampleReports.add
def table2(r):
    data = np.zeros((2, 2))
    r.table('mytable', data)

@ExampleReports.add
def table3(r):
    dtype = np.dtype([('field1', 'int32'), ('field2', 'int32')])
    data = np.zeros(shape=(5,), dtype=dtype)
    table = Table('mytable', data)
    r.add_child(table)

@ExampleReports.add
def imageRGB(r):
    rgb = np.zeros((4, 4, 3), 'uint8')
    r.data_rgb('rgb', rgb)

@ExampleReports.add
def imageRGBCaption(r):
    rgb = np.zeros((4, 4, 3), 'uint8')
    r.data_rgb('rgb', rgb, caption='ciao')

@ExampleReports.add
def figures1(r):
    rgb = np.zeros((4, 4, 3), 'uint8')
    f = r.figure()
    f.data_rgb('rgb', rgb, caption='ciao')
    # FIXME here
    r.data_rgb('rgb', rgb, caption='ciao2')
    r.last().add_to(f)

@ExampleReports.add
def figures0(r):
    rgb = np.zeros((4, 4, 3), 'uint8')
    f = r.figure()
    f.data_rgb('rgb1', rgb, caption='ciao')
    r.data_rgb('rgb2', rgb, caption='ciao2')
    r.data_rgb('rgb0', rgb, caption='ciao2')
    r.last().add_to(f)


@ExampleReports.add
def plot1(r):
    with r.plot('ciao') as pylab:
        pylab.plot([0, 1], [0, 1], '-k')

@ExampleReports.add
def plot2(r):
    with r.plot('ciao', caption='my caption') as pylab:
        pylab.plot([0, 1], [0, 1], '-k')

@ExampleReports.add
def text1(r):
    r.text('ciao', 'come va?')

@ExampleReports.add
def text2(r):
    r.text('ciao', 'come va?', MIME_PLAIN)
