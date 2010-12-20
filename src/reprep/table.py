import numpy

#from contracts import check_multiple

from .node import Node

class Table(Node):
    def __init__(self, id, data, cols=None, rows=None, caption=None):
        ''' 
            :type data:    ( array[R](fields[C]) | array[RxC] | list[R](list[C]) ), R>0, C>0
            :type cols:    None|list[C](str)
            :type rows:    None|list[R](str)
            :type caption: None|str 
        '''
        # :type data:    ( array[R](fields[C]) | array[RxC] | list[R](list[C]) ), R>0, C>0
            
        Node.__init__(self, id)
        
        if isinstance(data, list):
            # check minimum length
            if len(data) == 0:
                raise ValueError('Expected at least one row')
            # check that all of them are lists with same type
            for row in data:
                if not isinstance(row, list):
                    raise ValueError('Expected rows to be list, got %s' % \
                                     row.__class__.__name__)
                if not len(row) == len(data[0]):
                    raise ValueError('I want all rows to be the same length'\
                                     ' Got %s != %s.' % (len(row), len(data[0])))
            
            # create numpy array
            nrows = len(data)
            ncols = len(data[0])
            
            if ncols == 0:
                raise ValueError('At least one column expected')
            
#            dtype = map(lambda n: ('col%d' % n, numpy.object), range(ncols))
            
#            array = numpy.ndarray(shape=(nrows,), dtype=dtype)
#            for i in range(nrows):
#                for j in range(ncols):
#                    array[i][dtype[j][0]] = data[i][j]
#            data = array
#            array = numpy.ndarray(shape=(nrows, ncols), dtype=dtype)
#            for i in range(nrows):
#                for j in range(ncols):
#                    array[i, j] = data[i][j]
#            data = array
            
            if cols is None:
                cols = [None] * ncols
                
            if rows is None: 
                rows = [None] * nrows
                    
        elif isinstance(data, numpy.ndarray) :
            if not data.ndim in [1, 2]:
                raise ValueError('Expected array of 1D or 2D shape, got %s.' % 
                                describe_array(data))
                   
            if data.ndim == 1:             
                # use fields name if desc not provided
                if cols is None: # and data.dtype.fields is not None: 
                    cols = list(data.dtype.fields)
               
                nrows = len(data)
               
                if rows is None: 
                    rows = [None] * nrows
            
                lol = []
                for row in data:
                    lol.append(list(row))
                data = lol
                
            
            elif data.ndim == 2:
                if data.dtype.fields is not None: 
                    raise ValueError('Cannot convert ndarray to table using '
                                     'the heuristics that I know '
                                     '(received: %s). ' % describe_array(data))
                
                nrows = data.shape[0]
                ncols = data.shape[1]
                 
                if rows is None: rows = [None] * nrows
                if cols is None: cols = [None] * ncols
            
                data = data.tolist()
                
        else:
            raise ValueError('Expected list of lists or ndarray, got %s.' % 
                             data.__class__.__name__)
    

#        check_multiple([ (cols, 'list[C](str|None),C>0'),
#                         (rows, 'list[R](str|None),R>0'),
#                         (data, 'list[R](list[C])'),
#                         (caption, 'str|None') ])
        
        self.data = data
        self.cols = cols
        self.rows = rows
        self.caption = caption 

def describe_array(x):
    '''
        :type x: array
    '''
    return 'array[%s](%s)' % (x.shape, x.dtype)
    
