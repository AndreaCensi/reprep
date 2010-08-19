
from reprep.node import Node



class Table(Node):
    def __init__(self, id, data, col_desc=None, row_desc=None):
        Node.__init__(self, id)
        self.data = data
        self.col_desc = col_desc
        self.row_desc = row_desc
