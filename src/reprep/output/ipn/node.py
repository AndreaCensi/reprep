# -*- coding: utf-8 -*-
from reprep.figure import Figure
from reprep.table import Table
from reprep.node import Node
from reprep.datanode import DataNode

__all__ = ['report_to_ipn']

def report_to_ipn(report):
    context = IPNContext()
    node_to_ipn(report, context)


class IPNContext():
    def __init__(self, file,  # @ReservedAssignment
                 rel_resources_dir, resources_dir, write_pickle, pickle_compress):
        self.file = file
        self.rel_resources_dir = rel_resources_dir
        self.resources_dir = resources_dir
        self.write_pickle = write_pickle
        self.pickle_compress = pickle_compress


def datanode_to_ipn(node, context):
    from IPython.display import display, Image
    png = Image(data=r.resolve_url('graph/graph').get_raw_data(), format='png', embed=True)
    display(png)


def table_to_ipn(node, context):
    pass

def figure_to_ipn(node, context):
    pass

def simple_node_to_ipn(node, context):
    pass

def node_to_ipn(node, context):
    functions = {
        DataNode: datanode_to_ipn,
        Table: table_to_ipn,
        Figure: figure_to_ipn,
        Node: simple_node_to_ipn,
    }
    t = node.__class__
    if not t in functions:
        msg = ('Could not find type of %s (%s) in %s.' %
               (node, t, functions.keys()))
        raise ValueError(msg)
    functions[t](node, context)



