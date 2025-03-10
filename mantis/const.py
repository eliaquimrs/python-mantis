from operator import contains, eq, ne, ge, gt, lt, le
from enum import Enum


class BaseStrEnum(str, Enum):
    pass


# HTTP CONSTANTS
#   HTTP Methods
HTTP_METHOD_GET = 'GET'
HTTP_METHOD_POST = 'POST'
HTTP_METHOD_PUT = 'PUT'
HTTP_METHOD_DELETE = 'DELETE'
HTTP_METHOD_PATCH = 'PATCH'

#    HTTP Status codes
HTTP_MIN_SUCCESS_STATUS_CODE = 200
HTTP_MAX_SUCCESS_STATUS_CODE = 299
HTTP_MIN_CLIENT_ERROR_STATUS_CODE = 400
HTTP_MAX_CLIENT_ERROR_STATUS_CODE = 499
HTTP_MIN_SERVER_ERROR_STATUS_CODE = 500
HTTP_MAX_SERVER_ERROR_STATUS_CODE = 599


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


def not_contains(x, y): return not contains(x, y)


OPERATORS_MAP = {
    'contains': contains,
    'in': contains,
    'not contains': not_contains,
    'not in': not_contains,
    'eq': eq,
    '==': eq,
    '!=': ne,
    'ne': ne,
    '>=': ge,
    'ge': ge,
    '>': gt,
    'gt': gt,
    '<': lt,
    'lt': lt,
    '<=': le,
    'le': le
}

CONDITIONS_MAP = {
    "or": any,
    "and": all
}
