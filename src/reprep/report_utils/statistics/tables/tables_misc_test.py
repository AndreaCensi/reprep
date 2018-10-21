# -*- coding: utf-8 -*-
from reprep.demos.manager import reprep_demo
from reprep.report_utils.storing.store_results import StoreResults
from reprep.report_utils.statistics.structures.with_description import WithDescription
from reprep.report_utils.statistics.tables.tables_misc import table_by_rows


s1 = StoreResults()
s1[dict(algo='algo1', sample='sample1', delta=1)] = dict(time=1, objective=0)
s1[dict(algo='algo2', sample='sample1', delta=1)] = dict(time=2, objective=1)
s1[dict(algo='algo1', sample='sample2', delta=1)] = dict(time=3, objective=3)
s1[dict(algo='algo2', sample='sample2', delta=1)] = dict(time=4, objective=6)
s1[dict(algo='algo1', sample='sample3', delta=2)] = dict(time=5, objective=5)
s1[dict(algo='algo2', sample='sample3', delta=2)] = dict(time=6, objective=4)
s1[dict(algo='algo1', sample='sample4', delta=2)] = dict(time=7, objective=3)
s1[dict(algo='algo2', sample='sample4', delta=2)] = dict(time=8, objective=2)

descs = []
descs.append(WithDescription(name='algo', desc='Algorithm name', symbol=None)) 
descs.append(WithDescription(name='sample', desc='Sample ID', symbol=None))
descs.append(WithDescription(name='time', desc='Execution time', symbol='T'))
descs.append(WithDescription(name='objective', desc='Objective', symbol='J'))


descs.append(WithDescription(name='algo1', desc='One algo', symbol='A1'))
descs.append(WithDescription(name='algo2', desc='Other algo', symbol='A2'))

source_descs = dict((a.get_name(), a) for a in descs)


@reprep_demo
def table_multiple(r):
    table = table_by_rows(id_report="report", samples=s1,
                           rows_field='algo',
                           cols_fields=['time/all',
                                        'objective/max',
                                        'objective/min'],
                           source_descs=source_descs)
    r.add_child(table)
    
