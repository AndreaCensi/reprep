from . import VALID_ID_REGEXP
from contracts import new_contract
import re


@new_contract
def valid_id(s):
    assert isinstance(s, str)

    if re.match(VALID_ID_REGEXP, s) is None:
        msg = ('The given string %r does not match the spec %r.' % 
               (s, VALID_ID_REGEXP))
        raise ValueError(msg)
