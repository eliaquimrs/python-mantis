from __future__ import annotations

import operator
from typing import TypeVar, Generic, Any, Union, List, Set

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
        _parent: Union[ObjectBase, None] = None
    ) -> None:
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
            if attr.startswith('{') and attr.endswith('}'):
                value = attr.format(**self.__dict__)
                for pattern, value_to_replace in (
                    ('{', ''), ('}', ''), ('[', '.'), (']', '')
                ):
                    attr = attr.replace(pattern, value_to_replace)
            else:
                value = self.get(attr, "")

            attrs.append(f'{attr}={value}')

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
        if isinstance(other, type(self)):
            return condition(self._id, other._id)

        return NotImplemented

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

    def __hash__(self):
        return hash(self._id)


TObjBaseClass = TypeVar('TObjBaseClass', bound=ObjectBase)


class ObjectManagerBase(Generic[TObjBaseClass]):
    _path: str = None
    _id_attr: str = 'id'
    _key_response: Union[tuple[str], None] = None

    _mandatory_attr: tuple[str] = tuple()
    _optional_attr: tuple[str] = tuple()

    _readonly_attr: tuple[str] = tuple()

    _obj_cls: type[TObjBaseClass]
    _managed_obj_lst: Set[TObjBaseClass] = set()

    _parent_id_attr: str = None

    _child_manager_cls: Union[ObjectManagerBase[Any], None] = None

    _fixed_criteria: dict[str, Any] = {}

    def __init__(
        self,
        request: MantisRequests,
        manager_parent_obj: Union[TObjManagerClass, None] = None
    ):
        self.request = request
        self._manager_parent_obj = manager_parent_obj

        if self._child_manager_cls:
            self._child_manager_obj = self._child_manager_cls(request, self)

    def has_parent(self):
        return bool(self._manager_parent_obj and self._parent_id_attr)

    def _get_parent_obj_if_exist(self, obj: TObjBaseClass, _parent_obj=None):
        if self.has_parent():
            if not _parent_obj:
                parent_id = obj.get(self._parent_id_attr)
                if parent_id:
                    _parent_obj = self._manager_parent_obj.get_by_id(parent_id)

        return _parent_obj

    def _update_cache(self, obj: TObjBaseClass) -> None:
        if obj in self._managed_obj_lst:
            self._managed_obj_lst.remove(obj)
            self._managed_obj_lst.add(obj)
        else:
            self._managed_obj_lst.add(obj)

    def _get_object_from_cache(self, id_: Any) -> Union[TObjBaseClass, None]:
        obj = None

        fake_obj = self._obj_cls(self, {'id': id_})
        if fake_obj in self._managed_obj_lst:
            obj = self._managed_obj_lst.pop(fake_obj)
            self._managed_obj_lst.add(obj)

        return obj


TObjManagerClass = TypeVar('TObjManagerClass', bound=ObjectManagerBase)
