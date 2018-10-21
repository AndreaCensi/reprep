# -*- coding: utf-8 -*-
from .constants import MIME_PDF, MIME_SVG, MIME_PNG  # @UnusedImport


__all__ = ['RepRepDefaults']


class RepRepDefaults:
    savefig_params = dict(dpi=200, bbox_inches='tight', pad_inches=0.01,
                          transparent=True)

    default_image_format = MIME_PDF

    save_extra_png = True
    save_extra_pdf = False
    save_extra_svg = False

