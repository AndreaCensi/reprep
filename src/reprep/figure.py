from . import Node, DataNode, contract, describe_type, MIME_PYTHON
from collections import namedtuple
import warnings
from . import MIME_IMAGES

SubFigure = namedtuple('SubFigure',
                       'resource image caption display display_args')


class Figure(Node):

    @contract(cols='None|(int,>0)')
    def __init__(self, nid=None, caption=None, cols=None):
        Node.__init__(self, nid=nid)
        self.caption = caption
        self.cols = cols

        self.subfigures = []
        self.automatically_added = set()

    @contract(nid='valid_id', mime='None|str', caption='None|str')
    def data(self, nid, data, mime=MIME_PYTHON, caption=None):
        ''' Overloaded from Node. Displays the node automatically
            if it can be displayed.  '''

        child = Node.data(self, nid=nid, data=data, mime=mime, caption=caption)

        if (isinstance(child, DataNode) and
            (child.get_suitable_image_representation()
             or child.mime in MIME_IMAGES)):
            self.sub(child, child.caption)
            self.automatically_added.add(child)
        else:
            # XXX: what to do now?
            # print('Warning, not adding %s to figure.' % child)
            pass
        return child

    def sub(self, resource, caption=None, display=None, **kwargs):
        ''' Adds a subfigure displaying the given resource. 
        
            resource can either be a string or a data node.
        '''

        if isinstance(resource, str):
            data = self.resolve_url(resource)
        elif isinstance(resource, Node):
            data = resource
        else:
            raise ValueError('The first parameter to sub() must be either'
                             ' a string (url) or a reference to a Node, '
                             ' not a %s.' % describe_type(resource))

        if caption is None:
            caption = data.caption
            if caption is None:
                caption = data.nid

        if data in self.automatically_added:
            warnings.warn('Node %r was automatically added to figure (new '
                          'behavior in 1.0).' %
                          self.get_relative_url(data), stacklevel=2)
            return

        if not isinstance(data, DataNode):
            msg = ('I expect a DataNode as an argument to sub(), not a %s.'
                   % describe_type(resource))
            raise ValueError(msg)
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

        # TODO: check it is not already here
        sub = SubFigure(resource=resource_url, image=image_url,
                                caption=caption,
                               display=display, display_args=kwargs)
        self.subfigures.append(sub)

    def get_subfigures(self):
        return self.subfigures

