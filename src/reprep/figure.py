from collections import namedtuple
from reprep.node import Node, DataNode

SubFigure = namedtuple('SubFigure', 'resource image caption display display_args')

class Figure(Node):

    def __init__(self, id=None, caption=None, shape=None):
        Node.__init__(self, id=id)
        self.caption = caption
        self.shape = shape
        self.subfigures = []

    def sub(self, resource, caption=None, display=None, **kwargs):
        ''' Adds a subfigure displaying the given resource. '''
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
                
                self.parent.print_tree()
                raise ValueError('Could not find candidate image for resource '
                                 '"%s" image node is "%s".' % 
                                 (resource, data.get_complete_id()))
        
        resource_url = self.get_relative_url(data)
        image_url = self.get_relative_url(image)    
        
        sub = SubFigure(resource=resource_url, image=image_url,
                                caption=caption,
                               display=display, display_args=kwargs)
        self.subfigures.append(sub)  
