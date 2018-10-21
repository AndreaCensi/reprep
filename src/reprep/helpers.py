# -*- coding: utf-8 -*-
import mimetypes
import tempfile

from contracts import contract
from reprep import MIME_JPG, MIME_SVG, MIME_PDF, MIME_PNG, RepRepDefaults

from .datanode import DataNode
from .mpl import get_pylab_instance
from .node import Node

__all__ = ['PylabAttacher', 'Attacher']


class Attacher(object):

    @contract(node=Node, nid='valid_id', mime='None|str', caption='None|str')
    def __init__(self, node, nid, mime, caption):
        self.node = node
        self.nid = nid
        self.mime = mime
        self.caption = caption
        if node.has_child(nid):
            msg = 'Node %s (id = %r) already has child %r' % (node, node.nid, nid)
            raise ValueError(msg)
        if self.mime is not None:
            suffix = mimetypes.guess_extension(self.mime)

            if not suffix:
                raise Exception('Cannot guess extension for MIME %r.' % mime)

            if self.mime == MIME_JPG:
                suffix = '.jpg'

            # sometimes it returns 'svgz'...
            if self.mime == 'image/svg+xml':
                suffix = '.svg'

            # sometimes it returns '.txt'
            if self.mime == 'text/plain':
                suffix = '.txt'

            #             print('suffix for %r = %r' % (self.mime, suffix))

            if suffix == '.svgz':
                suffix = '.svg'
        else:
            suffix = '.bin'

        self.temp_file = tempfile.NamedTemporaryFile(suffix=suffix)

    def __enter__(self):
        return self.temp_file.name

    def __exit__(self, _a, _b, _c):
        with open(self.temp_file.name, 'rb') as f:
            data = f.read()
            self.node.data(nid=self.nid, data=data,
                           mime=self.mime,
                           caption=self.caption)
        self.temp_file.close()


class PylabAttacher(object):

    @contract(node=Node, nid='valid_id', mime='None|str', caption='None|str')
    def __init__(self, node, nid, mime, caption, **figure_args):
        self.node = node
        self.nid = nid
        self.mime = mime
        self.caption = caption

        if self.mime is None:
            self.mime = RepRepDefaults.default_image_format

        if node.has_child(nid):
            raise ValueError('Node %s already has child %r' % (node, nid))

        suffix = mimetypes.guess_extension(self.mime)
        if not suffix:
            msg = 'Cannot guess extension for MIME %r.' % mime
            raise ValueError(msg)

        self.temp_file = tempfile.NamedTemporaryFile(suffix=suffix)

        self.pylab = get_pylab_instance()
        self.figure = self.pylab.figure(**figure_args)

    def __enter__(self):
        return self.pylab

    def __exit__(self, exc_type, exc_value, traceback):  # @UnusedVariable
        if exc_type is not None:
            # an error occurred. Close the figure and return false.
            self.pylab.close()
            return False

        if not self.figure.axes:
            raise Exception('You did not draw anything in the image.')

        self.pylab.savefig(self.temp_file.name,
                           **RepRepDefaults.savefig_params)

        with open(self.temp_file.name, 'rb') as f:
            data = f.read()
        self.temp_file.close()

        image_node = DataNode(nid=self.nid, data=data,
                              mime=self.mime, caption=self.caption)

        # save other versions if needed
        if (self.mime != MIME_PNG) and RepRepDefaults.save_extra_png:
            with image_node.data_file('png', mime=MIME_PNG) as f2:
                self.pylab.savefig(f2, **RepRepDefaults.savefig_params)

        if (self.mime != MIME_SVG) and RepRepDefaults.save_extra_svg:
            with image_node.data_file('svg', mime=MIME_SVG) as f2:
                self.pylab.savefig(f2, **RepRepDefaults.savefig_params)

        if (self.mime != MIME_PDF) and RepRepDefaults.save_extra_pdf:
            with image_node.data_file('pdf', mime=MIME_PDF) as f2:
                self.pylab.savefig(f2, **RepRepDefaults.savefig_params)

        self.pylab.close()

        self.node.add_child(image_node)

        self.node.add_to_autofigure(image_node)


@contract(parent=Node, nid='valid_id',
          rgb='array[HxWx(3|4)]', caption='None|str')
def data_rgb_imp(parent, nid, rgb, mime=MIME_PNG, caption=None):
    from .graphics import Image_from_array, rgb_zoom

    # zoom images smaller than 50
    if max(rgb.shape[0], rgb.shape[1]) < 50:  # XXX config
        rgb = rgb_zoom(rgb, 10)

    pil_image = Image_from_array(rgb)

    with parent.data_file(nid=nid, mime=mime, caption=caption) as f:
        if mime == MIME_PNG:
            params = {}
        if mime == MIME_JPG:
            params = dict(quality=95, optimize=True)
        pil_image.save(f, **params)

    return parent[nid]
