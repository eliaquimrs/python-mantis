"""_summary_"""

__all__ = [ 'UnsupportedProtocolError' ]

from mantis import const

class UnsupportedProtocolError(Exception):
    def __init__(self,
                 protocol: str,
                 supported_protocols: list[str] = const.SUPPORTED_PROTOCOLS
    ):
        super().__init__(
            f'Protocol `{protocol}` is not supported! '
            f'Use one of supported protocol list: {supported_protocols}'
        )
