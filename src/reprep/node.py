from collections import namedtuple
import tempfile
import mimetypes
from graphics import posneg, Image_from_array
from reprep.graphics.success import colorize_success
import sys

class NotExistent(Exception):
    pass
class InvalidURL(Exception):
    pass


class NodeInterface: 
 
    def data(self, id, data, mime=None, desc=None):
        ''' Attaches a data node. "data" is assumed to be a raw python structure. 
            Or, if data is a string, pass a proper mime type ('image/png'). '''
        n = DataNode(id=id, data=data, mime=mime)
        self.add_child(n) 
        return n
    
    def data_file(self, id, mime):
        ''' Support for attaching data from a file. 
        This method is supposed to be used in conjunction with the "with"
        construct. 
        
        For example, the following is the concise way to attach a pdf
        plot to a node.::
        
            with report.data_file('plot', 'application/pdf') as f:
                pylab.figure()
                pylab.plot(x,y)
                pylab.savefig(f)
        
        Omit any file extension from 'id', ("plot" and not "plot.pdf"), we 
        will take care of it for you.
        
        This is a more complicated example, where we attach two versions
        of the same image, in different formats::
         
            for format in ['application/pdf', 'image/png']:
                with report.data_file('plot', format) as f:
                    pylab.figure()
                    pylab.plot(x,y)
                    pylab.savefig(f)

        '''
        return Attacher(self, id, mime)
 
    def figure(self, id, *args, **kwargs):
        f = Figure(id, *args, **kwargs)
        self.add_child(f) 
        return f
 
    def table(self, id, data, col_desc=None, row_desc=None):
        t = Table(id, data, col_desc, row_desc)
        self.add_child(t) 
        return t
        
    def add_child(self, n):
        ''' Adds a child to this node. Usually you would not use this
            method directly. '''
        n.parent = self
        self.children.append(n)

    
    
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
         
class Node(NodeInterface):
    def __init__(self, id=None, children=None):
        self.id = id
        if children is None:
            children = []
        self.children = []
        for c in children:
            self.add_child(c)
        self.parent = None
    
    def resolve_url_dumb(self, url):
        if not isinstance(url, str):
            raise ValueError('I expect a string, not %s.' % url)
        
        components = Node.url_split(url)
        if len(components) > 1:
            child = self.resolve_url_dumb(components[0])
            return child.resolve_url_dumb(Node.url_join(components[1:]))
        else:
            id = components[0]
            if id == '':
                raise InvalidURL()
            if id == '..':
                if self.parent:
                    return self.parent
                else:
                    raise NotExistent('No parent.')
                
            l = dict([(child.id, child) for child in self.children])
            if not id in l:
                if self.id == id:
                    return self
        
                raise NotExistent('Could not find child "%s".' % id)
            return l[id]
    
    def resolve_url(self, url, already_visited=None):
        if not isinstance(url, str):
            raise ValueError('I expect a string, not %s.' % url)
        if already_visited is None:
            already_visited = [self]
        else:
            if self in already_visited:
                raise NotExistent(url)
            already_visited += [self]
        
        if url.find('..') >= 0:
            # if it starts with .. we assume it's a precise url
            # and we don't do anything smart to find it
            return self.resolve_url_dumb(url)
        
        try: 
            return self.resolve_url_dumb(url)
        except NotExistent:
            pass
        
        for child in self.children:
            try:
                return child.resolve_url(url, already_visited=already_visited)
            except NotExistent:
                pass
            
        if self.parent:
            return self.parent.resolve_url(url, already_visited=already_visited)
        else:
            # in the end, we get here
            raise NotExistent('Could not find url "%s".' % url)
                
        
    @staticmethod        
    def url_split(u):    
        return u.split('/')

    @staticmethod
    def url_join(l):
        if not isinstance(l, list):
            raise ValueError('I expect a list, got "%s" (%s).' % (l, type(l)))
        return "/".join(l)

    def get_relative_url(self, other):
        assert isinstance(other, Node)
        if self == other:
            raise ValueError('I will not give you a relative url for myself.')
        all_my_parents = self.get_all_parents()
        
        if other in all_my_parents:
            levels = len(all_my_parents) - all_my_parents.index(other)
            url = Node.url_join(['..'] * levels)
            return url
        
        all_his_parents = other.get_all_parents()
        
        if self in all_his_parents:
            his_remaining = all_his_parents[all_his_parents.index(self) + 1:]
            components = [x.id for x in his_remaining] + [other.id]
            url = Node.url_join(components)
            return url
        
        common = [x for x in all_my_parents if x in all_his_parents]
        if not common:
            raise ValueError('The two nodes have no parents in common.')
        closest = common[-1]
        levels = len(all_my_parents) - all_my_parents.index(closest) 
        his_remaining = all_his_parents[all_his_parents.index(closest) + 1:]
        components = ['..'] * levels + [x.id for x in his_remaining] + [other.id]
        url = Node.url_join(components)
        
        try:
            assert self.resolve_url_dumb(url) == other
        except NotExistent:
            raise AssertionError('Produced url "%s" but does not work.' % url)
            
        return url
    
    def get_all_parents(self):
        ''' Returns a list of all parents. '''
        if self.parent:
            return self.parent.get_all_parents() + [self.parent]
        else:
            return []
        
    def print_tree(self, s=sys.stdout, prefix=""):
        s.write('%s- %s (%s)\n' % (prefix, self.id, self.__class__))
        for child in self.children:
            child.print_tree(s, prefix + '  ')
        
    def get_complete_id(self, separator=":"):
        if not self.parent:
            return self.id
        else:
            return self.parent.get_complete_id() + separator + self.id

    
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
            
        data = self.resolve_url(resource)
        
        if not isinstance(data, DataNode):
            raise ValueError('I expect a data node as an argument to sub(). (%s)' \
                             % resource)
        if display is not None:
            image = data.create_display(display, **kwargs)
        else:
            image = data.get_suitable_image_representation()
            if image is None:
                raise ValueError('Could not find candidate image for "%s".' % 
                                 resource)
        
        resource_url = self.get_relative_url(data)
        image_url = self.get_relative_url(image)    
        
        sub = SubFigure(resource=resource_url, image=image_url,
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
    def __init__(self, id, data, mime=None):
        Node.__init__(self, id)
        self.raw_data = data
        if mime is None:
            mime = 'python'
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
            
        return self.resolve_url_dumb(id)
        
    def get_suitable_image_representation(self):
        ''' Returns the node if it is an image; otherwise it looks recursively
            in the children. '''
        def is_image(node):
            return isinstance(node, DataNode) and node.mime.startswith('image')
        return self.find_recursively(is_image)

    def find_recursively(self, criterium):
        ''' Finds the closest node in the family passing the criterium.'''
        if criterium(self):
            return self
        else:
            for child in self.children:
                res = child.find_recursively(criterium)
                if res is not None:
                    return res
            return None

