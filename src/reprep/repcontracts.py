import re

from contracts import contract, new_contract
from zuper_commons.types import check_isinstance
from .constants import VALID_ID_REGEXP
from .types import NID

__all__ = ["sanitize_id", "valid_id"]


@new_contract
def valid_id(s):
    check_isinstance(s, str)

    if re.match(VALID_ID_REGEXP, s) is None:
        msg = "The given string %r does not match the spec %r." % (s, VALID_ID_REGEXP)
        raise ValueError(msg)


@contract(returns="valid_id")
def sanitize_id(nid: str) -> NID:
    nid = nid.replace("/", "_")
    nid = nid.replace(".", "_")
    return NID(nid)
