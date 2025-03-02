from enum import Enum


class BaseStrEnum(str, Enum):
    pass


class HTTP(BaseStrEnum):
    METHOD_GET = 'GET'
    METHOD_POST = 'POST'
    METHOD_PUT = 'PUT'
    METHOD_DELETE = 'DELETE'
    METHOD_PATCH = 'PATCH'


class REST(BaseStrEnum):
    HEADER_CONTENT_TYPE_JSON = 'application/json'
    HEADER_ACCEPT = '*/*'
    HEADER_USER_AGENT = 'python-mantis'
    HEADER_CONNECTION_KEEP_ALIVE = 'keep-alive'
    HEADER_CONNECTION_CLOSE = 'close'


class API_INFO_V1(BaseStrEnum):
    PATH = 'api/rest'
    VERSION = 'v1'

    PROJECTS_PATH = 'projects'

    ISSUES_PATH = 'issues'


API = dict(
    v1=API_INFO_V1
)

SUPPORTED_PROTOCOLS = [
    'http',
    'https'
]
