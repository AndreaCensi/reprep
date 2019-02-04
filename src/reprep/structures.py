# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class ReprepException(Exception):
    pass


class NotExistent(ReprepException):
    pass


class InvalidURL(ReprepException):
    pass
 
