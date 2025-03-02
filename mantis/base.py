from __future__ import annotations

import operator
from typing import TypeVar, Generic, Any, Union

from mantis._requests.mantis_requests import MantisRequests


__all__ = ['ObjectBase', 'ObjectManagerBase']


class ObjectBase:
    _repr_attrs: list[str] = ['id', 'title']
    _read_only_obj: bool = False

    _parent: Union[ObjectBase, None] = None

    manager: ObjectManagerBase[Any]

    def __init__(
            self,
            manager: ObjectManagerBase,
            attrs: dict[Any],
            _parent: Union[ObjectBase, None] = None,
    ):
        self.manager = manager
        self._parent = _parent

        for attr_name in self._get_all_attrs_definition():
            self.__setitem__(attr_name, attrs.get(attr_name, None), True)

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value, force=False) -> None:
        if not force:
            if self._read_only_obj:
                # TODO: Create a owner Exception
                raise AttributeError(
                    f'Object {self.__class__.__name__} is read only'
                )
            if key in self.readonly_attr:
                raise AttributeError(
                    f'Attribute {key} is read only'
                )

        self.__dict__[key] = value

    @property
    def mandatory_attrs(self):
        return self.manager._mandatory_attr

    @property
    def optional_attrs(self):
        return self.manager._optional_attr

    @property
    def readonly_attr(self):
        return self.manager._readonly_attr

    def __contains__(self, item):
        return item in self.__dict__

    def _get_all_attrs_definition(self):
        return (list(self.mandatory_attrs)
                + list(self.optional_attrs))

    def _parse_attrs_to__repr(self):
        attrs = []
        for attr in self._repr_attrs:
            attrs.append(f'{attr}={self.get(attr, "")}')

        return ', '.join(attrs)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def __repr__(self):
        attrs_to_repr = self._parse_attrs_to__repr()

        class_name = self.__class__.__name__
        if class_name.endswith('Obj'):
            class_name = class_name.replace('Obj', '')

        return f'{class_name}({attrs_to_repr})'

    # TODO: Reimplement __repr__ method
    def __str__(self):
        return self.__repr__()

    def _condition(self, other, condition):
        return condition(self._id, other._id)

    def __lt__(self, other):
        return self._condition(other, operator.lt)

    def __le__(self, other):
        return self._condition(other, operator.le)

    def __eq__(self, other):
        return self._condition(other, operator.eq)

    def __gt__(self, other):
        return self._condition(other, operator.gt)

    def __ge__(self, other):
        return self._condition(other, operator.ge)

    def __ne__(self, other):
        return self._condition(other, operator.ne)

    @property
    def _id(self):
        return self[self.manager._id_attr]

    def to_dict(self):
        _dict = {}
        for attr in self._get_all_attrs_definition():
            _dict[attr] = self.get(attr)

        return _dict


TObjBaseClass = TypeVar('TObjBaseClass', bound=ObjectBase)


class ObjectManagerBase(Generic[TObjBaseClass]):
    _path: str = None
    _id_attr: str = 'id'
    _key_response: str = None

    _mandatory_attr: tuple[str] = tuple()
    _optional_attr: tuple[str] = tuple()

    _readonly_attr: tuple[str] = tuple()

    _obj_cls: type[TObjBaseClass]

    _manage_parent_cls: Union[TObjManagerClass, None] = None

    def __init__(
        self,
        request: MantisRequests,
        manage_parent_obj: Union[TObjManagerClass, None] = None
    ):
        self.request = request
        pass

    def has_manage_parent(self):
        return bool(self._manage_parent_cls)


TObjManagerClass = TypeVar('TObjManagerClass', bound=ObjectManagerBase)
