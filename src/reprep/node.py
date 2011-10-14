from . import MIME_PNG, MIME_PYTHON, contract
from .graphics import Image_from_array, colorize_success, posneg, scale
from .interface import ReportInterface
import sys


 
class NotExistent(Exception):
    pass

class InvalidURL(Exception):
    pass
 

         
class Node(ReportInterface):
    
    @contract(nid='valid_id|None')
    def __init__(self, nid=None, children=None):
        
        if children is not None and not isinstance(children, list):
            raise ValueError('Received a %s object as children list, should'
                             ' be None or list.' % children.__class__.__name__)
        
        self.nid = nid 
        
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
        if n.nid is not None:
            if n.nid in self.childid2node:
                raise Exception('Already have child with same id %s.' % n.nid.__repr__())
        else:
            # give it a name
            n.nid = "%s%s" % (n.__class__.__name__, len(self.children))
            assert not n.nid in self.childid2node
            
        n.parent = self
        self.childid2node[n.nid] = n
        self.children.append(n)

    def last(self):
        ''' Returns the last added child Node. '''
        return self.children[-1]

    def node(self, nid):
        ''' Creates a simple child node. '''
        from . import Node
        n = Node(nid)
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
            nid = components[0]
            if nid == '':
                raise InvalidURL()
            if nid == '..':
                if self.parent:
                    return self.parent
                else:
                    raise NotExistent('No parent.')
                
            l = dict([(child.nid, child) for child in self.children])
            if not nid in l:
                if self.nid == nid:
                    return self
        
                raise NotExistent('Could not find child %r.' % nid)
            return l[nid]
    
    @contract(url='str')
    def resolve_url(self, url, already_visited=None):
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
        return self.resolve_url(relative_url)
        
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
            components = [x.nid for x in his_remaining] + [other.nid]
            url = Node.url_join(components)
            return url
        
        common = [x for x in all_my_parents if x in all_his_parents]
        if not common:
            raise ValueError('The two nodes have no parents in common.')
        closest = common[-1]
        levels = len(all_my_parents) - all_my_parents.index(closest) 
        his_remaining = all_his_parents[all_his_parents.index(closest) + 1:]
        components = ['..'] * levels + [x.nid for x in his_remaining] + [other.nid]
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
        s.write('%s- %s (%s)\n' % (prefix, self.nid, self.__class__))
        for child in self.children:
            child.print_tree(s, prefix + '  ')
        
    def get_complete_id(self, separator=":"):
        if not self.parent:
            return self.nid
        else:
            return self.parent.get_complete_id() + separator + self.nid

def just_check_rgb(value):
    ''' return value, checking it's a rgb image '''
    # TODO
    return value
    
        
class DataNode(Node):
    def __init__(self, nid, data, mime=None, caption=None):
        Node.__init__(self, nid)
        self.raw_data = data
        if mime is None:
            mime = MIME_PYTHON
        self.mime = mime
        self.caption = caption

    def display(self, display, **kwargs):
        if display is None:
            display = 'posneg'
        known = {'posneg': posneg,
                 'success': colorize_success,
                 'scale': scale,
                 'rgb': just_check_rgb}
        if not display in known:
            raise ValueError('No known converter %r. ' % display)
        nid = display # TODO: check; add args in the name

        image = known[display](self.raw_data, **kwargs) 
        #print image.dtype, image.shape
        pil_image = Image_from_array(image)  

        with self.data_file(nid, MIME_PNG) as f:
            pil_image.save(f)
            
        return self.resolve_url_dumb(nid)
        
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

