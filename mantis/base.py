from __future__ import annotations

import sys
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

        for k, v in attrs.items():
            self.__dict__[k] = v

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value) -> None:
        if self._read_only_obj:
            raise AttributeError(
                f'Object {self.__class__.__name__} is read only'
            )

        self.__dict__[key] = value

    def __repr__(self):
        attrs = ' - '.join(
            map(str, [self[repr_attr] for repr_attr in self._repr_attrs])
        )

        return f'<{self.__class__.__name__}({attrs})>'

    # TODO: Reimplement __repr__ method
    def __str__(self):
        return self.__repr__()

    def __lt__(self, other):
        return self._id < other._id

    def __le__(self, other):
        return self._id <= other._id

    def __eq__(self, other):
        return self._id == other._id

    def __gt__(self, other):
        return self._id > other._id

    def __ge__(self, other):
        return self._id >= other._id

    def __ne__(self, other):
        return self._id != other._id

    @property
    def _id(self):
        return self[self.manager._id_attr]


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
