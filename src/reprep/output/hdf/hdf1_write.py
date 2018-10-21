# -*- coding: utf-8 -*-
from . import write_python_data
from reprep import DataNode, Figure, __version__, Table
import datetime
import os
from reprep.output.hdf import get_tables


def to_hdf(node, filename):
    """ Writes the report in HDF format. """
    tables = get_tables()
    tmp_filename = filename + '.active'
    filters = tables.Filters(complevel=9, shuffle=False,
                            fletcher32=True, complib='zlib')
    hf = tables.openFile(tmp_filename, 'w', filters=filters)
    node_to_hdf(hf, hf.root, node)    

    hf.close()
    os.rename(tmp_filename, filename)

# FIXME: this is not checked yet
def ob2h5(x):
    """ If x is None, returns "None", otherwise x """
    if x is None:
        return 'None'
    else: 
        return x
    
import numpy as np

def node_to_hdf(hf, parent, node):
    group = hf.createGroup(where=parent, name=node.nid, title=node.caption)
    attrs = group._v_attrs 
    attrs['reprep_format_version'] = np.array([1, 0], dtype='int8')
    attrs['reprep_version'] = str(__version__)
    attrs['reprep_date_created'] = datetime.datetime.now().isoformat()
    attrs['reprep_node_type'] = node.__class__.__name__
    attrs['reprep_format_desc'] = """
    
    Node attributes:
        reprep_format_version: 
        reprep_version: 2 integers, major and minor.
        reprep_node_type: Type of node (Node, DataNode, Figure, Table)
        reprep_date_created: Current date
        reprep_order: order in which it appears in the report
        
    Protocol:
    
        [1, 0]:  First protocol.
        
    """

    if isinstance(node, DataNode):
        write_python_data(group, 'data', node.mime, node.raw_data)

    if isinstance(node, Table):
        hf.createArray(group, 'cols', node.cols, title='Headers for rows')
        hf.createArray(group, 'rows', node.rows, title='Headers for columns')
        hf.createArray(group, 'table_data', node.data)
        
    if isinstance(node, Figure):
        ncols = 0 if node.cols is None else node.cols
        hf.createArray(group, 'ncols', ncols, title='Number of columns')
        subfigures = hf.createGroup(group, 'subfigures')
        for i, s in enumerate(node.subfigures):
            sgroup = hf.createGroup(subfigures, 'sub%d' % i)
            hf.createArray(sgroup, 'resource', ob2h5(s.resource))
            hf.createArray(sgroup, 'image', ob2h5(s.image))
            hf.createArray(sgroup, 'web_image', ob2h5(s.web_image))
            hf.createArray(sgroup, 'caption', ob2h5(s.caption))

    for i, child in enumerate(node.children):
        cgroup = node_to_hdf(hf, parent=group, node=child)
        cgroup._v_attrs['reprep_order'] = i

    return group

# Node: nid, caption
# DataNode: nid, caption, data, mime
# DataNode: nid, caption, data, mime
# Figure: nid, caption, cols, subfigures
# Subfigures: (resource, image, web_image, caption)
# Table: nid, caption, cols, rows


