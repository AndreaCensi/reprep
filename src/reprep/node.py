from collections import namedtuple
#from odict import odict
import tempfile
import mimetypes
from graphics import posneg, Image_from_array
from reprep.graphics.success import colorize_success

class NodeInterface: 
           
    def data(self, id, data, mime='python', desc=None):
        ''' Adds python data. '''
        n = DataNode(id=id, data=data, mime=mime)
        self.add_child(n) 
        return n
    
    def add_child(self, n):
        n.parent = self
        self.children.append(n)

    def data_file(self, id, mime):
        ''' Adds file data. '''
        class Attacher:
            def __init__(self, node, id, mime):
                self.node = node
                self.id = id
                self.mime = mime
                if self.mime is not None:
                    suffix = mimetypes.guess_extension(self.mime)
                else:
                    suffix = '.bin'
                
                self.temp_file = tempfile.NamedTemporaryFile(suffix=suffix)
                
            def __enter__(self):
                return self.temp_file.name
                
            def __exit__(self, type, value, traceback): #@UnusedVariable
                with open(self.temp_file.name) as f:
                    data = f.read()
                    self.node.data(id=self.id, data=data, mime=self.mime)
                self.temp_file.close()
        return Attacher(self, id, mime)
 

    def figure(self, id, *args, **kwargs):
        f = Figure(id, *args, **kwargs)
        self.add_child(f) 
        return f

    def table(self, id, *args, **kwargs):
        t = Table(id, *args, **kwargs)
        self.add_child(t) 
        return t
        
class Node(NodeInterface):
    def __init__(self, id=None, children=None):
        self.id = id
        if children is None:
            children = []
        self.children = []
        for c in children:
            self.add_child(c)
        self.parent = None
    
    class NotExistent(Exception):
        pass
    class InvalidURL(Exception):
        pass
    
    def resolve_url(self, url):
        components = url_split(url)
        if len(components) > 1:
            child = self.resolve_url(components[0])
            return child.resolve_url(url_join(components[1:]))
        else:
            id = components[0]
            if id == '':
                raise Node.InvalidURL()
            l = dict([(child.id, child) for child in self.children])
            if not id in l:
                raise Node.NotExistent('Could not find child "%s".' % id)
            return l[id]
            
def url_split(u):    
    return u.split('/')

def url_join(l):
    if not isinstance(l, list):
        raise ValueError('I expect a list, got "%s" (%s).' % (l, type(l)))
    return "/".join(l)

SubFigure = namedtuple('SubFigure', 'resource image caption display display_args')

class Figure(Node):

    def __init__(self, id=None, caption=None, shape=None):
        Node.__init__(self, id=id)
        self.caption = caption
        self.shape = shape
        self.subfigures = []

    def sub(self, resource, caption=None, display=None, **kwargs):
        if caption is None:
            caption = resource
            
        data = self.parent.resolve_url(resource)
        if display is not None:
            rname = data.create_display(display, **kwargs)
            actual_resource = url_join([resource, rname])
        else:
            actual_resource = resource
        sub = SubFigure(resource=resource, image=actual_resource,
                                caption=caption,
                               display=display, display_args=kwargs)
        self.subfigures.append(sub)  
      

class Table(Node):
    def __init__(self, id, data, col_desc=None, row_desc=None):
        Node.__init__(self, id)
        self.data = data
        self.col_desc = col_desc
        self.row_desc = row_desc
        
class DataNode(Node):
    def __init__(self, id, data, mime='python'):
        Node.__init__(self, id)
        self.raw_data = data
        self.mime = mime

    def create_display(self, display, **kwargs):
        if display is None:
            display = 'posneg'
        known = {'posneg': posneg, 'success': colorize_success}
        if not display in known:
            raise ValueError('No known converter "%s". ' % display)
        id = display # TODO: check; add args in the name

        image = known[display](self.raw_data, **kwargs) 
        #print image.dtype, image.shape
        pil_image = Image_from_array(image)  

        with self.data_file(id, 'image/png') as f:
            pil_image.save(f)
            
        return id
        
