# -*- coding: utf-8 -*-
from . import get_tables, node_from_hdf_group_v1


def report_from_hdf(filename):
    tables = get_tables()
    hf = tables.openFile(filename, 'r')

    children = hf.root._v_children
    if len(children) == 0:
        msg = 'No groups in the root: %s' % hf
        raise Exception(msg)
    if len(children) > 1:
        msg = 'More than one child found: %s' % children
        raise Exception(msg)
    
    child = children[children.keys()[0]]
    node = node_from_hdf_group(hf, child)

    hf.close()
    return node

def node_from_hdf_group(hf, group):
    version = group._v_attrs['reprep_format_version']
    major = version[0]
    if major == 1:
        return node_from_hdf_group_v1(hf, group)
    else:
        msg = 'Cannot read from version %s' % version
        raise ValueError(msg)
