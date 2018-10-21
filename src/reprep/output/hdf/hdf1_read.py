# -*- coding: utf-8 -*-
from . import read_python_data
from reprep import DataNode, Node, Figure, SubFigure, Table
 
        
def node_from_hdf_group_v1(hf, group):
    major = group._v_attrs['reprep_format_version'][0]
    if major != 1:
        raise ValueError('I can oly read v1, not %s' % major)
    
    nid = group._v_name
    caption = group._v_title
    cgroups = [child for child in group._f_listNodes('Group')
               if 'reprep_format_version' in child._v_attrs]
    cgroups.sort(key=lambda x: x._v_attrs['reprep_order'])
    
    children = [node_from_hdf_group_v1(hf, child) for child in cgroups]
        
    nodetype = group._v_attrs['reprep_node_type']
    if nodetype == 'Node':
        return Node(nid=nid, children=children, caption=caption)
    
    elif nodetype == 'Figure':
        cols = group.ncols.read()
        if cols == 0: 
            cols = None
        figure = Figure(nid=nid, caption=caption, cols=cols)
        nsubs = len(group.subfigures._f_listNodes())
        for i in range(nsubs):
            s = group.subfigures._v_children['sub%d' % i]
            sub = SubFigure(resource=s.resource.read(),
                            image=s.image.read(),
                            web_image=s.web_image.read(),
                            caption=s.caption.read())
            figure.subfigures.append(sub)
        figure.children = children
        return figure
    
    elif nodetype == 'Table':
        table_data = group.table_data.read()
        rows = group.rows.read()
        cols = group.cols.read()
        table = Table(nid, data=table_data, cols=cols, rows=rows, caption=caption)
        table.children = children
        return table

    elif nodetype == 'DataNode':
        mime, raw_data = read_python_data(group, 'data')
        res = DataNode(nid=nid, data=raw_data, mime=mime, caption=caption)
        res.children = children
        return res
    else:
        raise ValueError('Unknown node_type %r' % nodetype)

