from enum import Enum


class BaseStrOwnEnum(str, Enum):
    pass


class REST(BaseStrOwnEnum):
    CONTENT_TYPE_JSON = 'application/json'


SUPPORTED_PROTOCOLS = [
    'http',
    'https'
]

if '__main__' in __name__:
    from json import dumps

    dict_test = {'content-type': REST.CONTENT_TYPE_JSON}
    print(dumps(dict_test))
