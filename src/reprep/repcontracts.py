# -*- coding: utf-8 -*-
from reprep import VALID_ID_REGEXP
from contracts import new_contract, contract
import re

__all__ = ['valid_id', 'sanitize_id']

@new_contract
def valid_id(s):
    assert isinstance(s, str)

    if re.match(VALID_ID_REGEXP, s) is None:
        msg = ('The given string %r does not match the spec %r.' % 
               (s, VALID_ID_REGEXP))
        raise ValueError(msg)

@contract(returns='valid_id')
def sanitize_id(nid):
    nid = nid.replace('/', '_')
    nid = nid.replace('.', '_')
    return nid
