from typing import cast

from zuper_commons.text import MimeType

MIME_PNG = cast(MimeType, "image/png")
MIME_JPG = cast(MimeType, "image/jpeg")
MIME_GIF = cast(MimeType, "image/gif")
MIME_PDF = cast(MimeType, "application/pdf")
MIME_RST = cast(MimeType, "text/x-rst")
MIME_PLAIN = cast(MimeType, "text/plain")
MIME_PYTHON = cast(MimeType, "application/python")
MIME_SVG = cast(MimeType, "image/svg+xml")
MIME_MP4 = cast(MimeType, "video/mp4")
MIME_GRAPHML = cast(MimeType, "application/graphml+xml")

MIME_GRAPHVIZ = cast(MimeType, "text/vnd.graphviz")

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
VALID_ID_REGEXP = r"\A\w(\w|-|\.)*\Z"


def mime_implies_unicode_representation(x):
    return x in [MIME_PLAIN, MIME_RST, MIME_SVG, MIME_GRAPHVIZ]
