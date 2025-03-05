"""__summary__"""
from typing import Union
from urllib.parse import urljoin

from mantis import utils, const
from mantis.api.v1 import objects as objects_v1
from mantis._requests import MantisRequests


class MantisBT:
    """A client for interacting with the MantisBT API.

    Attributes:
        _base_url (str): Base URL of the MantisBT instance.
        _requests (MantisRequests): Instance of MantisRequests for making API calls.

        timeout (Union[str, None]): Request timeout value.
        url (str): Full API URL.
        api_version (str): Version of MantisBT API being used.
        protocol (str): Protocol used to communicate with the MantisBT server.

        objects (module): Loaded objects for the current API version.
        projects (ProjectManager): Manager for project-related operations.
        issues (IssueManager): Manager for issue-related operations.
        configs (ConfigManager): Manager for configuration-related operations.
        filters (FilterManager): Manager for filter-related operations.
        notes (NoteManager): Manager for note-related operations.
        users (UserManager): Manager for user-related operations.

    Methods:
        __init__(url, user_api_token, timeout=None, mantis_api_version='v1'):
            Initialize a new MantisBT API client.
        get_api_url():
            Constructs and returns the full API URL.
        enable_debug(hide_credencials=True) -> None:
            Enables debug logging.
    """

    def __init__(
            self,
            url: str,
            user_api_token: str,
            timeout: Union[str, None] = None,
            mantis_api_version: str = 'v1'
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

        self.url = self.get_api_url()

        self._requests = MantisRequests(
            self.url, self._auth, self.timeout)

        self.objects = self._get_objects_cls()

        self.projects = self.objects.ProjectManager(self._requests)
        self.issues = self.objects.IssueManager(self._requests)
        self.configs = self.objects.ConfigManager(self._requests)
        self.filters = self.objects.FilterManager(self._requests)
        self.notes = self.objects.NoteManager(self._requests)
        self.users = self.objects.UserManager(self._requests)

    def _get_objects_cls(self):
        """Get the objects module for the current API version.

        Returns:
            API objects module: API module for the current API version
        """
        if self._mantis_api_version == 'v1':
            return objects_v1

    def get_api_url(self):
        """Get full URL of the MantisBT API (including mantis version).

        Returns:
            str: Full URL of the MantisBT API
        """
        return urljoin(self._base_url, const.API[self._mantis_api_version].PATH)

    @property
    def api_version(self) -> str:
        """Returns the MantisBT API version being used"""
        return self._mantis_api_version

    @property
    def protocol(self) -> str:
        """Returns the protocol used to communication with mantis server"""
        return self._server_protocol

    # TODO: Implement this method
    def enable_debug(self, hide_credencials: bool = True) -> None:
        """Enables debug logging"""
        pass
