from .with_description import WithDescription

__all__ = [
    "FunctionWithDescription",
]


class FunctionWithDescription(WithDescription):
    """A function with a description"""

    def __init__(self, function, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.function = function
