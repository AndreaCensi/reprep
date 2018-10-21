# -*- coding: utf-8 -*-
from .node import Node
from contracts import check_isinstance, contract, describe_value
import numpy as np


__all__ = [
    'Table',
] 

class Table(Node):
    
    @contract(nid='valid_id', caption='None|str')
    def __init__(self, nid, data, cols=None, rows=None, fmt=None, caption=None):
        ''' 
            :type data:  (array[R](fields[C]) | array[RxC] | list[R](list[C])
                 ), R>0, C>0
            :type cols:    None|list[C](str)
            :type rows:    None|list[R](str)
            :type caption: None|str 
        '''

        if fmt is None:
            fmt = '%s'
        self.fmt = fmt

        Node.__init__(self, nid)
        
        check_isinstance(data, (list, np.ndarray))

        if isinstance(data, list):
            # check minimum length
            if len(data) == 0:
                raise ValueError('Expected at least one row')
            # check that all of them are lists with same type
            for row in data:
                check_isinstance(row, list)
                if not len(row) == len(data[0]):
                    msg = ('I want all rows to be the same length'
                          ' Got %s != %s.' % (len(row), len(data[0])))
                    raise ValueError(msg)

            # create numpy array
            nrows = len(data)
            ncols = len(data[0])

            if ncols == 0:
                raise ValueError('At least one column expected')

            if cols is None:
                cols = [''] * ncols

            if rows is None:
                rows = [''] * nrows

        elif isinstance(data, np.ndarray):
            if not data.ndim in [1, 2]:
                msg= ('Expected array of 1D or 2D shape, got %s.' % 
                        describe_value(data))
                raise ValueError(msg)

            if data.ndim == 1:
                # use fields name if desc not provided
                if cols is None:  # and data.dtype.fields is not None: 
                    cols = list(data.dtype.fields)

                nrows = len(data)

                if rows is None:
                    rows = [''] * nrows

                lol = []
                for row in data:
                    lol.append(list(row))
                data = lol

            elif data.ndim == 2:
                if data.dtype.fields is not None:
                    msg = ('Cannot convert ndarray to table using '
                            'the heuristics that I know (received: %s). ' 
                            % describe_value(data))
                    raise ValueError(msg)

                nrows = data.shape[0]
                ncols = data.shape[1]

                if rows is None:
                    rows = [''] * nrows
                if cols is None:
                    cols = [''] * ncols

                data = data.tolist()

        else:
            assert False
            
#
#         check_multiple([ (cols, 'list[C](str|None),C>0'),
#                          (rows, 'list[R](str|None),R>0'),
#                          (data, 'list[R](list[C])'),
#                          (caption, 'str|None') ])
#         print('cols', cols)
#         print('rows', rows)
#         print('data', data)
#         print('cols', cols)

        self.data = data
        self.cols = cols
        self.rows = rows
        self.caption = caption



def table_from_array(r, nid, a):
    data = []
    cols = list(a.dtype.names)
    
    for v in a:
        row = [v[n] for n in cols]
        data.append(row)
    
    rows = ['']* len(data)
    r.table(nid, data, cols, rows, fmt=None, caption=None)
