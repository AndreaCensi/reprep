from . import write_python_data, tables
from reprep import DataNode, Figure, __version__, Table
import datetime
import os


def to_hdf(node, filename):
    """ Writes the report in HDF format. """
    tmp_filename = filename + '.active'
    hf = tables.openFile(tmp_filename, 'w')
    node_to_hdf(hf, hf.root, node)
#    
#    filters_text = tables.Filters(complevel=1, shuffle=False,
#                                    fletcher32=False, complib='zlib')

    hf.close()
    if os.path.exists(filename):
        os.unlink(filename)
    os.rename(tmp_filename, filename)

# FIXME: this is not checked yet
def ob2h5(x):
    """ If x is None, returns "None", otherwise x """
    if x is None:
        return 'None'
    else: 
        return x
    
    
def node_to_hdf(hf, parent, node):
    group = hf.createGroup(where=parent, name=node.nid, title=node.caption)
    attrs = group._v_attrs 
    attrs['reprep_format_version'] = [1, 0]
    attrs['reprep_version'] = str(__version__)
    attrs['reprep_date_created'] = datetime.datetime.now().isoformat()
    attrs['reprep_node_type'] = node.__class__.__name__
    attrs['reprep_format_desc'] = """
    
    Node attributes:
        reprep_format_version: 
        reprep_version: 2 integers, major and minor.
        reprep_node_type: Type of node (Node, DataNode, Figure, Table)
        reprep_date_created: Current date
        
    Protocol:
    
        [1, 0]:  First protocol.
        
    """
    
#    
#    meta = hf.createGroup(group, '_reprep', title='Meta-information for RepRep')
#    hf.createArray(meta, 'reprep_version', str(reprep.__version__),
#                   title='Version of RepRep package')
#    hf.createArray(meta, 'format_version', [1, 0],
#                   title='Major and minor version of RepRep protocol')
#    hf.createArray(meta, 'date_created', datetime.datetime.now().isoformat(),
#                   title='Current date')
#    hf.createArray(meta, 'node_type', node.__class__.__name__,
#                   "Type of node (Node, DataNode, Figure, Table)")

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

    for child in node.children:
        print('Writing %s' % child)
        node_to_hdf(hf, parent=group, node=child)


# Node: nid, caption
# DataNode: nid, caption, data, mime
# DataNode: nid, caption, data, mime
# Figure: nid, caption, cols, subfigures
# Subfigures: (resource, image, web_image, caption)
# Table: nid, caption, cols, rows


