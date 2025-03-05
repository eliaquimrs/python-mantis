"""This module provides the MantisRequests class for making HTTP requests 
        with custom error handling.

Classes:
    MantisRequests: A class for making HTTP requests with custom headers,
        error handling, and session management.

Raises:
    MantisHTTPReponseClientError: Raised for HTTP client errors (4xx).
    MantisHTTPReponseServerError: Raised for HTTP server errors (5xx).
    MantisHTTPError: (Generic) Raised for other HTTP errors.
    MantisConnectionTimeout: Raised when a connection times out.
    MantisConnectionError: Raised for connection errors.
    MantisReadTimeout: Raised when a read operation times out.
"""

from copy import deepcopy
from json import dumps as json_dumps
from sys import version_info
from typing import Union, Any

from requests import Session, Request, Response
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout

from mantis import const, __title__
from mantis.exceptions import (
    MantisConnectionError, MantisConnectionTimeout, MantisReadTimeout,
    MantisHTTPReponseClientError, MantisHTTPReponseServerError, MantisHTTPError
)


class MantisRequests:
    """A class for making HTTP requests with custom headers, error handling,
        and session management.

    Attributes:
        base_url (str): The base URL for the HTTP requests.
        auth (str): The authentication token for the HTTP requests.
        timeout (Union[float, int]): The timeout duration for the HTTP requests.
        http_header (dict): The default HTTP headers for the requests.
        _session (Session): The session object for managing HTTP connections.

    Methods:
        __init__(self, base_url: str, auth: str, timeout: Union[float, int]) -> None:
            Initializes the MantisRequests instance with base URL, authentication, and timeout.

        get_http_header(self) -> dict[Any]:
            Returns the default HTTP headers for requests.

        raise_http_error_by_status_code(self, response: Response, e: Exception):
            Raises an appropriate custom exception based on the HTTP status code.

        http_request(self, method: str, sufix_url_path: str, 
                params: Union[dict, None] = None, data: Union[dict, None] = None,
                extra_headers: Union[dict, None] = None, **kwargs):
            A generic method for making HTTP requests

        http_get(self, sufix_path: str, params: Union[dict, None] = None,
                                                                    **kwargs):
            Make an HTTP GET request

        http_post(self, sufix_path: str, params: Union[dict, None] = None,
                                     data: Union[dict, None] = None, **kwargs):
            Makes an HTTP POST request
    """

    def __init__(
        self,
        base_url: str,
        auth: str,
        timeout: Union[float, int]
    ) -> None:
        """Initializes the MantisRequests instance

        Args:
            base_url (str): Base URL for the HTTP requests.
            auth (str): Authentication token for the HTTP requests (for inclusion
                                              in headers `Authorization` field).
            timeout (Union[float, int]): Timeout duration for the HTTP requests
                                                       (in seconds). (optional)
        """
        self.base_url = base_url
        self.auth = auth
        self.timeout = timeout

        self.http_header = self.get_http_header()

        self._session = Session()

    def _get_user_agent(self) -> str:
        """Returns the user agent string for the HTTP requests. (Including 
                                 Python version + package name `python-mantis`)

        Returns:
            str: User agent string for the HTTP requests.
        """
        # Get major.minor.micro version numbers from sys.version_info
        py_version = f'{version_info.major}.{version_info.minor}.{version_info.micro}'

        if version_info.releaselevel != 'final':
            py_version += version_info.releaselevel

        return f'Python {py_version}/{__title__}'

    def get_http_header(self) -> dict[Any]:
        """Get the default HTTP headers for the requests.

        Returns:
            dict[Any]: Default HTTP headers for the requests.
        """
        headers = {
            'Accept': const.REST.HEADER_ACCEPT.value,
            'User-Agent': self._get_user_agent(),
            'Connection': const.REST.HEADER_CONNECTION_KEEP_ALIVE.value
        }
        if self.auth:
            headers['Authorization'] = self.auth

        return headers

    def _prepare_url(self, sufix_url_path: str) -> str:
        """Prepare the full URL for the HTTP requests.

        Args:
            sufix_url_path (str): The URL path to append to the base URL.

        Returns:
            str: The full URL for the HTTP request (base URL + Sufix URL path).
        """
        if sufix_url_path.startswith('/'):
            sufix_url_path = sufix_url_path[1:]

        return f'{self.base_url}/{sufix_url_path}'

    # TODO: Review: any other validation/manipulation needed for data?
    def _prepare_data(self, data: dict[Any]) -> str:
        """Prepare the data  for the HTTP requests.

        Args:
            data (dict[Any]): The data to be sent in the request.

        Returns:
            str: The JSON string representation of the data.
        """
        return json_dumps(data)

    def _get_header_for_request(
        self,
        extra_headers: Union[dict, None] = None
    ) -> dict[Any]:
        """Get the headers for the HTTP request.

        Args:
            extra_headers (Union[dict, None], optional): Extra arguments to 
                                 join for header default data. Defaults to None.

        Returns:
            dict[Any]: The headers for the HTTP request.
        """
        headers = deepcopy(self.http_header)

        if extra_headers:
            headers.update(extra_headers)

        return headers

    def raise_http_error_by_status_code(
        self,
        response: Response,
        e: Exception
    ):
        """Raise an appropriate custom exception based on the HTTP status code.

        Args:
            response (Response): The response object from the HTTP request.
            e (Exception): The exception object raised by the request module.

        Raises:
            MantisHTTPReponseClientError: Raised for HTTP client errors (4xx).
            MantisHTTPReponseServerError: Raised for HTTP server errors (5xx).
            MantisHTTPError: (Generic) Raised for other HTTP errors.
        """
        status = response.status_code
        if (
            status >= const.HTTP_MIN_CLIENT_ERROR_STATUS_CODE
            and status <= const.HTTP_MAX_CLIENT_ERROR_STATUS_CODE
        ):
            raise MantisHTTPReponseClientError(response, self, e)
        elif (
            status >= const.HTTP_MIN_SERVER_ERROR_STATUS_CODE
            and status <= const.HTTP_MAX_SERVER_ERROR_STATUS_CODE
        ):
            raise MantisHTTPReponseServerError(response, self, e)
        else:
            raise MantisHTTPError(response, self, e)

    def http_request(
            self,
            method: str,
            sufix_url_path: str,
            params: Union[dict, None] = None,
            data: Union[dict, None] = None,
            extra_headers: Union[dict, None] = None,
            **kwargs
    ) -> dict[Any]:
        """A generic method for making HTTP requests.

        Args:
            method (str): The HTTP method name to use for the request.
            sufix_url_path (str): The URL path to append to the base URL.
            params (Union[dict, None], optional): Parameters to include in the
                request. Defaults to None.
            data (Union[dict, None], optional): Data to include in the request.
                Defaults to None.
            extra_headers (Union[dict, None], optional): Extra headers to include
                in the request. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the request. (
                                               during mount of `Request` object)

        Raises:
            MantisConnectionTimeout: Raised when a connection with Mantis API
                                                                     times out.
            MantisConnectionError: Raised for connection errors with Mantis API.
            MantisReadTimeout: Raised when a read operation with Mantis API 
                                                                      times out.

        Returns:
            dict[Any]: The JSON response from the HTTP request.
        """
        url = self._prepare_url(sufix_url_path)
        headers = self._get_header_for_request(extra_headers)

        request_obj = Request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            **kwargs
        )
        preparred_request = self._session.prepare_request(request_obj)

        try:
            response = self._session.send(
                preparred_request, timeout=self.timeout)
        except ConnectTimeout as e:
            raise MantisConnectionTimeout(preparred_request, self, e)
        except ConnectionError as e:
            raise MantisConnectionError(preparred_request, self, e)
        except ReadTimeout as e:
            raise MantisReadTimeout(preparred_request, self, e)

        try:
            response.raise_for_status()
        except Exception as e:
            self.raise_http_error_by_status_code(response, e)

        if (
                response.status_code >= const.HTTP_MIN_SUCCESS_STATUS_CODE
            and response.status_code <= const.HTTP_MAX_SUCCESS_STATUS_CODE
        ):
            return response.json()

        # TODO: Validate redirections, etc.
        return response

    def http_get(
            self,
            sufix_path: str,
            params: Union[dict, None] = None,
            **kwargs
    ) -> dict[Any]:
        """Make an HTTP GET request.

        Args:
            sufix_path (str): The URL path to append to the base URL.
            params (Union[dict, None], optional): Parameters to include in the
                request. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the request. (
                                               during mount of `Request` object)

        Returns:
            dict[Any]: The JSON response from the HTTP request.
        """
        return self.http_request(const.HTTP_METHOD_GET,
                                 sufix_path, params=params, **kwargs)

    def http_post(
            self,
            sufix_path: str,
            params: Union[dict, None] = None,
            data: Union[dict, None] = None,
            **kwargs
    ):
        """ Makes an HTTP POST request.

        Args:
            sufix_path (str): The URL path to append to the base URL.
            params (Union[dict, None], optional): arameters to include in the
                request. Defaults to None.
            data (Union[dict, None], optional): Data to include in the request.
                Defaults to None.
            **kwargs: Additional keyword arguments to pass to the request. (
                                               during mount of `Request object)

        Returns:
            dict[Any]: The JSON response from the HTTP request.
        """
        extra_headers = kwargs.get('extra_headers', None)
        if data:
            extra_headers = extra_headers or {}
            extra_headers.update({
                'Content-Type': const.REST.HEADER_CONTENT_TYPE_JSON
            })

        return self.http_request(const.HTTP_METHOD_POST,
                                 sufix_path, params=params, data=data,
                                 extra_headers=extra_headers, **kwargs)
