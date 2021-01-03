from zuper_commons.types import ZException


class ReprepException(ZException):
    pass


class NotExistent(ReprepException):
    pass


class InvalidURL(ReprepException):
    pass
