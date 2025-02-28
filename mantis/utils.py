"""_summary_"""
from typing import Tuple
from urllib.parse import urlparse, ParseResult

from mantis import const
from mantis.exceptions import UnsupportedProtocolError


def mantis_url_parse(url: str) -> Tuple[str, ParseResult, str]:
    """Parse URL from mantis server

    Args:
        url (str): URL to access the mantis server HTTP API

    Raises:
        UnsupportedProtocolError: Raised while a protocol is not supported for 
            the MantisBT API

    Returns:
        Tuple[str, ParseResult, str]: Tuple with Protocol, url information
            parsed (by urllib module) and base_url to call the mantis server
    """
    url_parsed = urlparse(url)
    protocol = url_parsed.scheme

    if protocol not in const.SUPPORTED_PROTOCOLS:
        raise UnsupportedProtocolError(protocol)

    base_url = f'{protocol}://{url_parsed.netloc}/'

    return protocol, url_parsed, base_url


if '__main__' in __name__:
    print(mantis_url_parse('http://127.0.0.1'))
