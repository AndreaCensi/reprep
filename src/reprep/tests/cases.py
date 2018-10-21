# -*- coding: utf-8 -*-
from .. import Report
from .utils import fancy_test_decorator

__all__ = ['ExampleReports', 'for_all_example_reports']

class ExampleReports:
    """ Stores test cases; see for_all_example_reports """
    generators = {}

    @staticmethod 
    def add(generator):
        """ Use as decorator. """
        ExampleReports.generators[generator.__name__] = generator
        return generator


    @staticmethod
    def list_all():
        return list(ExampleReports.generators.keys())
    
    @staticmethod
    def get_params(eid):
        r = Report(eid)
        ExampleReports.generators[eid](r)
        return (r,)
    
    @staticmethod
    def get_attrs(eid):
        """ Returns test attributes """
        return dict(example=eid)


for_all_example_reports = fancy_test_decorator(lister=ExampleReports.list_all,
                                             arguments=ExampleReports.get_params,
                                             attributes=ExampleReports.get_attrs,
                                             debug=True)

 
                                                 
