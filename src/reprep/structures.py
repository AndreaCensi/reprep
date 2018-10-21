# -*- coding: utf-8 -*-

class ReprepException(Exception):
    pass


class NotExistent(ReprepException):
    pass


class InvalidURL(ReprepException):
    pass
 
