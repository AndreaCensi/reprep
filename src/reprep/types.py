from typing import NewType

from zuper_commons.text import MimeType

__all__ = [
    "MimeType",
    "NID",
]

NID = NewType("NID", str)
