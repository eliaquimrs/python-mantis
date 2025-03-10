"""_summary_"""
from urllib.parse import urlparse, ParseResult
from operator import contains
from typing import Tuple, Any, List, Union, Tuple, Literal

from mantis import const
from mantis.const import not_contains
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


def _parse_condition_value(value, obj):
    if isinstance(value, str) and value.startswith('{') and value.endswith('}'):
        return eval(value[1:-1])

    return value


# TODO: Create exceptions for invalid operator (contains, in, ==, etc)
def exec_condition(left_op, original_operator, right_op, obj):
    try:
        operator = const.OPERATORS_MAP[original_operator]
    except KeyError:
        raise Exception(f'Invalid operator: {original_operator}')

    try:
        left_data = _parse_condition_value(left_op, obj)
        right_data = _parse_condition_value(right_op, obj)
    except AttributeError:
        return False

    if operator in [contains, not_contains]:
        # Only string values are accepted for the  operator.contains
        left_data = str(left_data)
        right_data = str(right_data)

        # We use operator.contains to validate `in`/`not in` conditions
        #   for this reason, we need to invert the operator
        #   - User send: ('Project', 'in', '{obj.name}')
        #   - We execute: ('{obj.name}', 'contains', 'Project')
        if original_operator in ['in', 'not in']:
            # Invert right left data
            left_data, right_data = right_data, left_data

    return operator(left_data, right_data)


# TODO: Create exceptions for invalid condition structure
def filter_objects(
    objects,
    conditions: Union[List[Any], Tuple[Any], None] = None,
    main_condition: Literal['and', 'or'] = 'and'
):
    if main_condition == 'and':
        m_cond = all
    elif main_condition == 'or':
        m_cond = any

    filtred_objects = []
    for obj in objects:
        results = []
        for left_op, operator_str, right_op in conditions:
            results.append(
                exec_condition(left_op, operator_str, right_op, obj)
            )

        if m_cond(results):
            filtred_objects.append(obj)

    return filtred_objects
