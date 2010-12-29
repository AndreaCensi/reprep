import sys

from graphics import Image_from_array, colorize_success

from .interface import  ReportInterface
from reprep.graphics.scale import scale
from reprep.graphics.posneg import posneg
 
class NotExistent(Exception):
    pass

class InvalidURL(Exception):
    pass
   
         
class Node(ReportInterface):
    def __init__(self, id=None, children=None):
        if id is not None and not isinstance(id, str):
            raise ValueError('Received a %s object as ID, should be None or str.' % \
                            id.__class__.__name__)
        
        if children is not None and not isinstance(children, list):
            raise ValueError('Received a %s object as children list, should'\
                             ' be None or list.' % children.__class__.__name__)
        
        if isinstance(id, str):
            if '/' in id:
                raise ValueError('Invalid node id %r (contains "/").' % id)
            if len(id) == 0:
                raise ValueError('Cannot give an empty string as name.')
        
        self.id = id 
        
        if children is None:
            children = []
    
        self.childid2node = {}
        self.children = []
        for c in children:
            if not isinstance(c, Node):
                raise ValueError('Passed instance of class %s as child.' % c.__class__.__name__)
            self.add_child(c)
        self.parent = None
        
    def add_child(self, n):
        ''' Adds a child to this node. Usually you would not use this
            method directly. '''
        assert n is not None
        if n.id is not None:
            if n.id in self.childid2node:
                raise Exception('Already have child with same id %s.' % n.id.__repr__())
        else:
            # give it a name
            n.id = "%s%s" % (n.__class__.__name__, len(self.children))
            assert not n.id in self.childid2node
            
        n.parent = self
        self.childid2node[n.id] = n
        self.children.append(n)

    def last(self):
        ''' Returns the last added child Node. '''
        return self.children[-1]

    def node(self, id):
        ''' Creates a simple child node. '''
        from reprep import Node
        n = Node(id)
        self.add_child(n)
        return n 


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
                
    def __getitem__(self, relative_url):
        return self.get_relative_url(relative_url)
        
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

def just_check_rgb(value):
    ''' return value, checking it's a rgb image '''
    return value
    
        
class DataNode(Node):
    def __init__(self, id, data, mime=None):
        Node.__init__(self, id)
        self.raw_data = data
        if mime is None:
            mime = 'python'
        self.mime = mime

    def display(self, display, **kwargs):
        if display is None:
            display = 'posneg'
        known = {'posneg': posneg,
                 'success': colorize_success,
                 'scale': scale,
                 'rgb': just_check_rgb}
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

