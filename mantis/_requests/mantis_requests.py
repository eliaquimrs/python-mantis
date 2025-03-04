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
    def __init__(
        self,
        base_url: str,
        auth: str,
        timeout: Union[float, int]
    ) -> None:
        self.base_url = base_url
        self.auth = auth
        self.timeout = timeout

        self.http_header = self.get_http_header()

        self._session = Session()

    def _get_user_agent(self) -> str:
        # Get major.minor.micro version numbers from sys.version_info
        py_version = f'{version_info.major}.{version_info.minor}.{version_info.micro}'

        if version_info.releaselevel != 'final':
            py_version += version_info.releaselevel

        return f'Python {py_version}/{__title__}'

    def get_http_header(self) -> dict[Any]:
        headers = {
            'Accept': const.REST.HEADER_ACCEPT.value,
            'User-Agent': self._get_user_agent(),
            'Connection': const.REST.HEADER_CONNECTION_KEEP_ALIVE.value
        }
        if self.auth:
            headers['Authorization'] = self.auth

        return headers

    def _prepare_url(self, sufix_url_path: str) -> str:

        if sufix_url_path.startswith('/'):
            sufix_url_path = sufix_url_path[1:]

        return f'{self.base_url}/{sufix_url_path}'

    def _prepare_data(self, data: dict[Any]) -> str:
        return json_dumps(data)

    def _get_header_for_request(
        self,
        extra_headers: Union[dict, None] = None
    ) -> dict[Any]:
        headers = deepcopy(self.http_header)

        if extra_headers:
            headers.update(extra_headers)

        return headers

    def raise_http_error_by_status_code(
        self,
        response: Response,
        e: Exception
    ):
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
    ):
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

        return response

    def http_get(
            self,
            sufix_path: str,
            params: Union[dict, None] = None,
            **kwargs
    ):
        return self.http_request(const.HTTP_METHOD_GET,
                                 sufix_path, params=params, **kwargs)

    def http_post(
            self,
            sufix_path: str,
            params: Union[dict, None] = None,
            data: Union[dict, None] = None,
            **kwargs
    ):
        extra_headers = kwargs.get('extra_headers', None)
        if data:
            extra_headers = extra_headers or {}
            extra_headers.update({
                'Content-Type': const.REST.HEADER_CONTENT_TYPE_JSON
            })

        return self.http_request(const.HTTP_METHOD_POST,
                                 sufix_path, params=params, data=data,
                                 extra_headers=extra_headers, **kwargs)
