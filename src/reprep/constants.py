# -*- coding: utf-8 -*-
MIME_PNG = 'image/png'
MIME_JPG = 'image/jpeg'
MIME_PDF = 'application/pdf'
MIME_RST = 'text/x-rst'
MIME_PLAIN = 'text/plain'
MIME_PYTHON = 'application/python'
MIME_SVG = 'image/svg+xml'
MIME_MP4 = 'video/mp4'

MIME_GRAPHVIZ = 'text/vnd.graphviz'

# Images 
MIME_IMAGES = [MIME_PDF, MIME_SVG, MIME_PNG, MIME_JPG]
# Images that can be displayed in a browser
MIME_WEB_IMAGES = [MIME_SVG, MIME_PNG, MIME_JPG]

#VALID_ID_REGEXP = '\A\w+\Z'
#VALID_ID_REGEXP = '\A\w(\w|-)*\Z'
VALID_ID_REGEXP = '\A\w(\w|-|\.)*\Z'

