from reprep.node import Node
import numpy

class Table(Node):
    def __init__(self, id, data, cols=None, rows=None, caption=None):
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
            
            dtype = map(lambda n: ('col%d' % n, numpy.object), range(ncols))
            
            
            array = numpy.ndarray(shape=(nrows,), dtype=dtype)
            for i in range(nrows):
                for j in range(ncols):
                    array[i][dtype[j][0]] = data[i][j]
            data = array
            
            if cols is None:
                cols = [None] * ncols
                
            if rows is None: 
                rows = [None] * nrows
                    
        elif isinstance(data, numpy.ndarray) :
            if len(data.shape) != 1:
                raise Exception('Expected array of 1D shape, got %s.' % \
                                str(data.shape))
            # use fields name if desc not provided
            if cols is None:
                cols = list(data.dtype.fields)
           
            if rows is None: 
                rows = [None] * nrows
                
        else:
            raise ValueError('Expected list of list or ndarray, got %s' % \
                             data.__class__.__name__)
    
        if len(cols) != len(data.dtype.fields):
            raise ValueError('Expected cols of length %s, not %s' % \
                             (len(data.dtype.fields), str(cols)))
            
        # TODO: add unit tests for rows
        self.data = data
        self.cols = cols
        self.rows = rows
        self.caption = caption 


