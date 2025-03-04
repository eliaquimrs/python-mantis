"""_summary_"""

__all__ = ['UnsupportedProtocolError']

from typing import Any

from requests import PreparedRequest

from mantis import const


class MantisGenericError(Exception):
    ...


class MantisHTTPError(MantisGenericError):
    def __init__(
        self,
        response: Any,
        mantis_request_cls: Any,
        _original_exception: Exception = None
    ):
        self.response = response
        print(dir(_original_exception))
        self._request_cls = mantis_request_cls
        self._original_exception = _original_exception

        super().__init__(self.get_message())

    def get_message(self) -> str:
        return f'{self._original_exception}'


class MantisHTTPReponseClientError(MantisHTTPError):
    ...


class MantisHTTPReponseServerError(MantisHTTPError):
    ...


class MantisHTTPConnError(MantisGenericError):
    def __init__(
        self,
        preparred_request: PreparedRequest,
        mantis_request_cls: Any,
        _original_exception: Exception
    ):
        self.preparred_request = preparred_request
        self._original_exception = _original_exception
        self._request_cls = mantis_request_cls

        super().__init__(self.get_message())

    def get_message(self) -> str:
        return (f'Original Error: {self._original_exception}\n'
                f'Request data: {self._get_prepared_request_info()}')

    def _get_prepared_request_info(self) -> str:
        headers = self.preparred_request.headers
        headers.pop('Authorization', None)

        req_info = {
            'url': self.preparred_request.url,
            'method': self.preparred_request.method,
            'headers': headers,
            'data': self.preparred_request.body
        }
        return req_info


class MantisConnectionError(MantisHTTPConnError):
    ...


class MantisConnectionTimeout(MantisHTTPConnError):
    ...


class MantisReadTimeout(MantisHTTPConnError):
    ...


class UnsupportedProtocolError(MantisGenericError):
    def __init__(
        self,
        protocol: str,
        supported_protocols: list[str] = const.SUPPORTED_PROTOCOLS
    ):
        super().__init__(
            f'Protocol `{protocol}` is not supported! '
            f'Use one of supported protocol list: {supported_protocols}'
        )
