# -*- coding: utf-8 -*-
import mimetypes
import tempfile
from typing import Optional

from contracts import contract
from reprep import mime_implies_unicode_representation, RepRepDefaults
from zuper_commons.types import ZException
from .constants import MIME_JPG, MIME_PDF, MIME_PNG, MIME_SVG, mime_to_ext
from .datanode import DataNode
from .mpl import get_pylab_instance
from .node import Node

__all__ = ["PylabAttacher", "Attacher"]

from .types import MimeType, NID


class Attacher:
    node: Node
    nid: NID
    mime: Optional[MimeType]
    caption: Optional[str]

    def __init__(
        self, node: Node, nid: NID, mime: Optional[MimeType], caption: Optional[str]
    ):
        self.node = node
        self.nid = nid
        self.mime = mime
        self.caption = caption
        if node.has_child(nid):
            msg = "Node %s (id = %r) already has child %r" % (node, node.nid, nid)
            raise ValueError(msg)
        if self.mime is not None:
            if self.mime in mime_to_ext:
                suffix = "." + mime_to_ext[self.mime]
            else:
                suffix = mimetypes.guess_extension(self.mime)

                if not suffix:
                    msg = "Cannot guess extension for MIME %r." % mime
                    raise ZException(msg)

                if suffix == ".svgz":
                    suffix = ".svg"
        else:
            suffix = ".bin"

        self.temp_file = tempfile.NamedTemporaryFile(suffix=suffix)

    def __enter__(self):
        return self.temp_file.name

    def __exit__(self, _a, _b, _c):
        data = open(self.temp_file.name, "rb").read()

        if mime_implies_unicode_representation(self.mime):
            data = data.decode("utf-8")

        self.node.data(nid=self.nid, data=data, mime=self.mime, caption=self.caption)
        self.temp_file.close()


class PylabAttacher:
    node: Node
    nid: NID
    mime: Optional[MimeType]
    caption: Optional[str]

    @contract(node=Node, nid="valid_id", mime="None|unicode", caption="None|unicode")
    def __init__(
        self,
        node: Node,
        nid: NID,
        mime: Optional[MimeType],
        caption: Optional[str],
        **figure_args
    ):
        self.node = node
        self.nid = nid
        self.mime = mime
        self.caption = caption

        if self.mime is None:
            self.mime = RepRepDefaults.default_image_format

        if node.has_child(nid):
            raise ValueError("Node %s already has child %r" % (node, nid))

        suffix = mimetypes.guess_extension(self.mime)
        if not suffix:
            msg = "Cannot guess extension for MIME %r." % mime
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
            raise Exception("You did not draw anything in the image.")

        self.pylab.savefig(self.temp_file.name, **RepRepDefaults.savefig_params)

        with open(self.temp_file.name, "rb") as f:
            data = f.read()
        self.temp_file.close()

        image_node = DataNode(
            nid=self.nid, data=data, mime=self.mime, caption=self.caption
        )

        # save other versions if needed
        if (self.mime != MIME_PNG) and RepRepDefaults.save_extra_png:
            with image_node.data_file("png", mime=MIME_PNG) as f2:
                self.pylab.savefig(f2, **RepRepDefaults.savefig_params)

        if (self.mime != MIME_SVG) and RepRepDefaults.save_extra_svg:
            with image_node.data_file("svg", mime=MIME_SVG) as f2:
                self.pylab.savefig(f2, **RepRepDefaults.savefig_params)

        if (self.mime != MIME_PDF) and RepRepDefaults.save_extra_pdf:
            with image_node.data_file("pdf", mime=MIME_PDF) as f2:
                self.pylab.savefig(f2, **RepRepDefaults.savefig_params)

        self.pylab.close()

        self.node.add_child(image_node)

        self.node.add_to_autofigure(image_node)


@contract(parent=Node, nid="valid_id", rgb="array[HxWx(3|4)]")
def data_rgb_imp(
    parent: Node, nid: NID, rgb, mime=MIME_PNG, caption: Optional[str] = None
):
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
