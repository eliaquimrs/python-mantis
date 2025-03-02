from copy import deepcopy
from sys import version_info
from typing import Union
from urllib.parse import urljoin

import requests

from mantis import const, __title__


class MantisRequests:
    def __init__(self, base_url, auth, timeout):
        self.base_url = base_url
        self.auth = auth
        self.timeout = timeout

        self.http_header = self.get_http_header()

        self._session = requests.Session()

    def _get_user_agent(self):
        # Get major.minor.micro version numbers from sys.version_info
        py_version = f'{version_info.major}.{version_info.minor}.{version_info.micro}'

        if version_info.releaselevel != 'final':
            py_version += version_info.releaselevel

        return f'Python {py_version}/{__title__}'

    def get_http_header(self):
        headers = {
            'Accept': const.REST.HEADER_ACCEPT,
            'User-Agent': self._get_user_agent(),
            'Connection': const.REST.HEADER_CONNECTION_KEEP_ALIVE
        }
        if self.auth:
            headers['Authorization'] = self.auth

        return headers

    def _prepare_url(self, sufix_url_path: str):
        print(self.base_url, sufix_url_path)
        return f'{self.base_url}/{sufix_url_path}'
        return urljoin(self.base_url, sufix_url_path)

    def _get_header_for_request(self, extra_headers: Union[dict, None] = None):
        headers = deepcopy(self.http_header)

        if extra_headers:
            headers.update(extra_headers)

        return headers

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
        print(url)

        headers = self._get_header_for_request(extra_headers)

        response = self._session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            timeout=self.timeout,
            **kwargs
        )

        return response

    def http_get(
            self,
            sufix_path: str,
            params: Union[dict, None] = None,
            **kwargs
    ):
        return self.http_request(const.HTTP.METHOD_GET,
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

        return self.http_request(const.HTTP.METHOD_POST,
                                 sufix_path, params=params, data=data,
                                 extra_headers=extra_headers, **kwargs)
