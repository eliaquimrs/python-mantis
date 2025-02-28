"""__summary__"""
from typing import Union

from mantis import utils


class MantisBT:
    def __init__(
            self,
            url: str,
            user_api_token: str,
            timeout: Union[str, None] = None,
            mantis_api_version: str = ''
    ) -> None:
        """
        Initialize a new MantisBT API client.

        Args:
            url: Full URL of the MantisBT instance
            user_api_token: API token for authentication
            timeout: Request timeout value (optional)
            mantis_api_version: Version of MantisBT API to use (optional)
        """
        self._url = url
        self._server_protocol, self._url_information, self._base_url = \
            utils.mantis_url_parse(url)
        self._auth = user_api_token

        self._mantis_api_version = mantis_api_version
        self.timeout = timeout

    @property
    def api_version(self) -> str:
        """Returns the MantisBT API version being used"""
        return self._mantis_api_version

    @property
    def protocol(self) -> str:
        """Returns the protocol used to communication with mantis server"""
        return self._server_protocol

    def enable_debug(self, hide_credencials: bool = True) -> None:
        """Enables debug logging"""
        pass
