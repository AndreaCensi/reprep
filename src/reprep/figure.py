from collections import namedtuple
from warnings import warn

from .node import Node, DataNode

SubFigure = namedtuple('SubFigure', 'resource image caption display display_args')

class Figure(Node):

    def __init__(self, id=None, caption=None, shape=None, cols=None):
        Node.__init__(self, id=id)
        self.caption = caption
        
        if shape is not None:
            warn('Using deprecated parameter "shape" instead of "cols".')
            self.cols = shape[1]
        else:
            self.cols = cols 
        
        self.subfigures = []
        
        
    def sub(self, resource, caption=None, display=None, **kwargs):
        ''' Adds a subfigure displaying the given resource. 
        
            resource can either be a string or a data node.
        '''
        if caption is None:
            caption = resource
            
        if isinstance(resource, str):
            data = self.resolve_url(resource)
        elif isinstance(resource, Node):
            data = resource
        else:
            raise ValueError('The first parameter to sub() must be either'
                             ' a string (url) or a reference to a Node, '
                             ' not a %s.' % resource.__class__.__name__)
            
        
        if not isinstance(data, DataNode):
            raise ValueError('I expect a **data** node as an argument to sub(). (%s)' \
                             % resource)
        if display is not None:
            image = data.display(display, **kwargs)
        else:
            image = data.get_suitable_image_representation()
            
            if image is None:
                self.parent.print_tree()
                raise ValueError('Could not find candidate image for resource '
                                 '%r; image node is %r.' % 
                                 (resource, data.get_complete_id()))
        
        resource_url = self.get_relative_url(data)
        image_url = self.get_relative_url(image)    
        
        sub = SubFigure(resource=resource_url, image=image_url,
                                caption=caption,
                               display=display, display_args=kwargs)
        self.subfigures.append(sub)  
