import mantis
from mantis.__version import (
    __author__,
    __copyright__,
    __email__,
    __license__,
    __title__,
    __version__
)
from mantis.client import MantisBT
from mantis.exceptions import *

__all__ = [
    '__author__',
    '__copyright__',
    '__email__',
    '__license__',
    '__title__',
    '__version__',
    'MantisBT'
]
__all__.extend(mantis.exceptions.__all__)
