# -*- coding: utf-8 -*-


MIME_PNG = "image/png"
MIME_JPG = "image/jpeg"
MIME_GIF = "image/gif"
MIME_PDF = "application/pdf"
MIME_RST = "text/x-rst"
MIME_PLAIN = "text/plain"
MIME_PYTHON = "application/python"
MIME_SVG = "image/svg+xml"
MIME_MP4 = "video/mp4"
MIME_GRAPHML = "application/graphml+xml"

MIME_GRAPHVIZ = "text/vnd.graphviz"

# Images
MIME_IMAGES = [MIME_PDF, MIME_SVG, MIME_PNG, MIME_JPG, MIME_GIF]
# Images that can be displayed in a browser
MIME_WEB_IMAGES = [MIME_SVG, MIME_PNG, MIME_JPG, MIME_GIF]

mime_to_ext = {
    MIME_JPG: "jpg",
    MIME_SVG: "svg",
    MIME_PLAIN: "txt",
    MIME_GIF: "gif",
    MIME_GRAPHML: "graphml",
}

# VALID_ID_REGEXP = '\A\w+\Z'
# VALID_ID_REGEXP = '\A\w(\w|-)*\Z'
VALID_ID_REGEXP = "\A\w(\w|-|\.)*\Z"


def mime_implies_unicode_representation(x):
    return x in [MIME_PLAIN, MIME_RST, MIME_SVG, MIME_GRAPHVIZ]
