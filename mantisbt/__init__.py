import mantisbt

from mantisbt.__version import (
    __author__,
    __copyright__,
    __email__,
    __license__,
    __title__,
    __version__
)
from mantisbt.client import MantisBT
from mantisbt.exceptions import *

__all__ = [
    '__author__',
    '__copyright__',
    '__email__',
    '__license__',
    '__title__',
    '__version__',
    'MantisBT'
]
__all__.extend(mantisbt.exceptions.__all__)
