from __future__ import annotations

import operator
from typing import TypeVar, Generic, Any, Union, List, Set

from mantis._requests.mantis_requests import MantisRequests


__all__ = ['ObjectBase', 'ObjectManagerBase']


# LIST of TODOs:
# TODO: Create logic to mapping fields updated in the object, to be used in the `save()` method

# TODO: Implement convertion of attributes value in specific types (e.g: date, datetime, etc)
#       e.g: `created_at` attribute is a string, but should be a datetime object

# TODO: Implement a way to has multiple childs. e.g: In NoteObj we have a attribute called `reporter` this attribute should be a `UserObj` object

class ObjectBase:
    """A generic class to represent a object from Mantis.
    Use this class to create a object representation of a Mantis object.

    Atributes to be replaced in your own class:
        _repr_attrs (list[str]): List of attributes to be shown in __repr__ method (mandatory)
        _read_only_obj (bool): If True, object cannot be changed. Default False (optional)

    Atributes:
        manager (ObjectManagerBase): Manager of this object
        _parent (ObjectBase): The Parent object

        _id (Any): The id of the object
        mandatory_attrs (tuple[str]): List of mandatory attributes (obteined from manager object)
        optional_attrs (tuple[str]): List of optional attributes (obteined from manager object)
        readonly_attr (tuple[str]): List of read only attributes (obteined from manager object)

    Raises:
        AttributeError: If try to set a read only attribute or the object is read only
    """
    _repr_attrs: list[str] = ['id']
    _read_only_obj: bool = False

    _parent: Union[ObjectBase, None] = None

    manager: ObjectManagerBase[Any]

    def __init__(
        self,
        manager: ObjectManagerBase,
        attrs: dict[Any],
        _parent: Union[ObjectBase, None] = None
    ) -> None:
        """Create a new ObjectBase instance.

        Args:
            manager (ObjectManagerBase): The manager object of this object
            attrs (dict[Any]): The all attributes of the object
            _parent (Union[ObjectBase, None], optional): The parent object. Defaults to None.
        """
        self.manager = manager
        self._parent = _parent

        for attr_name in self._get_all_attrs_definition():
            self.__setitem__(attr_name, attrs.get(attr_name, None), True)

    def __getitem__(self, item):
        """Get the value of a attribute."""
        return self.__dict__[item]

    def __setitem__(self, key: Any, value: Any, force: bool = False) -> None:
        """Set the value of a attribute.

        Args:
            key (Any): The attribute name
            value (Any): The value to be set
            force (bool, optional): If True, the attribute can be set even if is read only. Defaults to False.

        Raises:
            AttributeError: If try to set a read only attribute or the object is read only
        """
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
        """List of mandatory attributes. (obteined from manager object)"""
        return self.manager._mandatory_attr

    @property
    def optional_attrs(self):
        """List of optional attributes. (obteined from manager object)"""
        return self.manager._optional_attr

    @property
    def readonly_attr(self):
        """List of read only attributes. (obteined from manager object)"""
        return self.manager._readonly_attr

    def __contains__(self, item: Any) -> bool:
        """Check if a attribute is in the object."""
        return item in self.__dict__

    def _get_all_attrs_definition(self) -> List[str]:
        """Get all attributes definition(mandatory + optional) from the manager object."""
        return (list(self.mandatory_attrs)
                + list(self.optional_attrs))

    def _parse_attrs_to__repr(self):
        """Parse the attributes (from _repr_attr) to be shown in __repr__ method.
            Use: {attr_name['<key>']} to get the value of a attribute.
                e.g: {reporter['name']} will get the value of the attribute 'name' from the attribute 'reporter'
                The representation will be: reporter.name=<value>
        """
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
        """Get the value of a attribute."""
        return self.__dict__.get(key, default)

    def _parse_class_name(self):
        """Parse the class name to be shown in __repr__ method."""
        class_name = self.__class__.__name__
        if class_name.endswith('Obj'):
            class_name = class_name.replace('Obj', '')

        return class_name

    def __repr__(self):
        """Return a string representation of the object."""
        attrs_to_repr = self._parse_attrs_to__repr()
        class_name = self._parse_class_name()

        return f'{class_name}({attrs_to_repr})'

    # TODO: Reimplement __str__ method
    def __str__(self):
        """Return a string representation of the object."""
        return self.__repr__()

    def _condition(self, other, condition):
        """Generic method to check the condition between two objects."""
        if isinstance(other, type(self)):
            return condition(self._id, other._id)

        return NotImplemented

    def __lt__(self, other):
        """Check if the object is less than other object. (<)"""
        return self._condition(other, operator.lt)

    def __le__(self, other):
        """Check if the object is less or equal than other object. (<=)"""
        return self._condition(other, operator.le)

    def __eq__(self, other):
        """Check if the object is equal to other object. (==)"""
        return self._condition(other, operator.eq)

    def __gt__(self, other):
        """Check if the object is greater than other object. (>)"""
        return self._condition(other, operator.gt)

    def __ge__(self, other):
        """Check if the object is greater or equal than other object. (>=)"""
        return self._condition(other, operator.ge)

    def __ne__(self, other):
        """Check if the object is different than other object. (!=)"""
        return self._condition(other, operator.ne)

    @property
    def _id(self):
        """Get the id of the object."""
        return self[self.manager._id_attr]

    def to_dict(self):
        """Return a dictionary representation of the object. Converting all attributes to a dictionary."""
        _dict = {}
        for attr in self._get_all_attrs_definition():
            _dict[attr] = self.get(attr)

        return _dict

    def _hash_string(self):
        """Return a string representation of the object to be used in the hash."""
        return f'{self.__class__.__name__}{self._id}'

    def __hash__(self):
        """ Return the hash of the classname + object._id. When a object is compareted, the hash is used to compare the objects.
                So, 2 diferent object but with the same class and ID will be considered the same object.
        """
        return hash(self._hash_string())


TObjBaseClass = TypeVar('TObjBaseClass', bound=ObjectBase)


class ObjectManagerBase(Generic[TObjBaseClass]):
    """A generic class to manage objects from Mantis.
    Use this class to create a manager representation of a Mantis object.

    Atributes to be replaced in your own class:
        _path (str): The path to the API endpoint (mandatory)
        _id_attr (str): The attribute that represents the id of the object (mandatory)
        _key_response (tuple[str]): The key/keys to be used to get the object
                                             from the Mantis response (optional)
        _mandatory_attr (tuple[str]): List of mandatory attributes (mandatory)
        _optional_attr (tuple[str]): List of optional attributes (mandatory)
        _readonly_attr (tuple[str]): List of read only attributes (optional)
        _obj_cls (type): The class of the objects to be managed (mandatory)
        _parent_id_attr (str): The attribute that represents the parent id (optional)
        _child_manager_cls (ObjectManagerBase): The manager of the child object (optional)
        _fixed_criteria (dict): Fixed filter/criteria to be used in the requests (optional)

    Atributes:
        _managed_obj_lst (set): The list of managed objects (internal cache)
        request (MantisRequests): The request object to be used in the manage
        _manager_parent_obj (ObjectManagerBase): The parent manager object
        _child_manager_obj (ObjectManagerBase): The child manager object

    """

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
        """Create a new ObjectManagerBase instance.

        Args:
            request (MantisRequests): The request object to be used in the manager
            manager_parent_obj (Union[TObjManagerClass, None], optional): The parent manager object. Defaults to None.
        """
        self.request = request
        self._manager_parent_obj = manager_parent_obj

        if self._child_manager_cls:
            self._child_manager_obj = self._child_manager_cls(request, self)

    def has_parent(self) -> bool:
        """Check if the manager has a parent object.

        Returns:
            bool: True if has parent, False otherwise
        """
        return bool(self._manager_parent_obj and self._parent_id_attr)

    def _get_parent_obj_if_exist(
        self,
        obj: TObjBaseClass,
        _parent_obj=None
    ) -> Union[TObjBaseClass, None]:
        """Get the parent object if exists.

        Args:
            obj (TObjBaseClass): The main object to get the parent
            _parent_obj (_type_, optional): The parent object (if already exists). Defaults to None.

        Returns:
            Union[TObjBaseClass, None]: The parent object or None
        """
        if self.has_parent():
            if not _parent_obj:
                parent_id = obj.get(self._parent_id_attr)
                if parent_id:
                    _parent_obj = self._manager_parent_obj.get_by_id(parent_id)

        return _parent_obj

    def _update_cache(self, obj: TObjBaseClass) -> None:
        """Update a internal cache of objects.

        Args:
            obj (TObjBaseClass): The object to be updated in the cache
        """
        if obj in self._managed_obj_lst:
            self._managed_obj_lst.remove(obj)
            self._managed_obj_lst.add(obj)
        else:
            self._managed_obj_lst.add(obj)

    def _get_object_from_cache(self, id_: Any) -> Union[TObjBaseClass, None]:
        """Get a object from the internal cache

        Args:
            id_ (Any): The id of the object to be get

        Returns:
            Union[TObjBaseClass, None]: The object or None
        """
        obj = None

        fake_obj = self._obj_cls(self, {'id': id_})
        if fake_obj in self._managed_obj_lst:
            obj = self._managed_obj_lst.pop(fake_obj)
            self._managed_obj_lst.add(obj)

        return obj


TObjManagerClass = TypeVar('TObjManagerClass', bound=ObjectManagerBase)


class ObjectListManager:
    """A class to manage lists of Mantis objects with iteration, filtering and sorting capabilities."""

    def __init__(self, objects: List[ObjectBase]):
        """Initialize with list of objects.

        Args:
            objects (List[ObjectBase]): List of Mantis objects to manage
        """
        self.objects = objects
        self.current_index = -1

    def __iter__(self):
        """Make class iterable."""
        return self

    def __next__(self) -> ObjectBase:
        """Get next object in list.

        Returns:
            ObjectBase: Next object in sequence

        Raises:
            StopIteration: When end of list is reached
        """
        self.current_index += 1
        if self.current_index >= len(self.objects):
            self.current_index = -1
            raise StopIteration
        return self.objects[self.current_index]

    def next(self) -> Union[ObjectBase, None]:
        """Get next object without raising StopIteration.

        Returns:
            Union[ObjectBase, None]: Next object or None if at end
        """
        try:
            return next(self)
        except StopIteration:
            return None

    def previous(self) -> Union[ObjectBase, None]:
        """Get previous object in list.

        Returns:
            Union[ObjectBase, None]: Previous object or None if at start
        """
        if self.current_index > 0:
            self.current_index -= 1
            return self.objects[self.current_index]
        return None

    # TODO: Predict more condition: e.g contains(in), !=, ==, etc
    def filter(self, *args) -> ObjectListManager:
        """Filter objects by attribute values.

        Args:
            **kwargs: Attribute names and values to filter by

        Returns:
            ObjectListManager: New manager with filtered objects
        """
        filtered = []
        for obj in self.objects:
            matches = True
            for key, value in kwargs.items():
                if obj.get(key) != value:
                    matches = False
                    break
            if matches:
                filtered.append(obj)
        return ObjectListManager(filtered)

    def sort(self, key: str, reverse: bool = False) -> ObjectListManager:
        """Sort objects by an attribute.

        Args:
            key (str): Attribute name to sort by
            reverse (bool): Sort in reverse order if True

        Returns:
            ObjectListManager: New manager with sorted objects
        """
        sorted_objects = sorted(
            self.objects,
            key=lambda x: x.get(key),
            reverse=reverse
        )
        return ObjectListManager(sorted_objects)

    def __len__(self) -> int:
        """Get number of objects in list."""
        return len(self.objects)

    def __getitem__(self, index: int) -> ObjectBase:
        """Get object at index."""
        return self.objects[index]

    def __repr__(self) -> str:
        """Return string representation of the list manager.

        Returns:
            str: String showing number of objects and current index
        """
        return f"ObjectListManager(objects={len(self.objects)}, current_index={self.current_index})"

    def __str__(self) -> str:
        """Return string representation showing all objects.

        Returns:
            str: String listing all managed objects
        """
        return "ObjectListManager%s" % self.objects
