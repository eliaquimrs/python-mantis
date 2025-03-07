"""Base mixins for object managers in the Mantis framework.

This module provides mixin classes that implement common functionality for object managers:
"""

from copy import deepcopy
from typing import Any, List

from mantis.base import ObjectManagerBase, ObjectBase


# TODO: Add support for pagination (limit of response)

# TODO: Add refresh method
#       1. Implement a method called `refresh` that will get new data from the server (method used in ObjectBase)

# TODO: Add support for update:
#       update_many (?)
#       update_one:
#       1. Mapping atrributes updated in the object (implement in ObjectBase?)
#       2. Implement a method called `save` that will update the object in the server
#       3. Call the method  `refresh` to get new data from the server ()

# TODO: Add support for delete
#    delete_many (?)
#    delete_one (?)

# TODO: Add support for create
#    - Create object in the server
#    - mandatory, optional and read-only fields must be used to create the object
#    - Default values to optional fields is necessary?
#    - Implement a method called `create` that will create the object in the server

class GetMixins(ObjectManagerBase):
    # TODO: Add a new parameter `search_for_parent`? (bool). If not, don't search
    #   in the mantis server the _parent object
    def _get(
        self,
        url: str,
        params: dict[str, Any] = None,
        _parent=None
    ) -> List[ObjectBase]:
        """The generic function to execute GET HTTP and retrieves a list of objects from a given URL with optional parameters.

        Args:
            url (str): The URL to send the GET request to.
            params (dict[str, Any], optional): A dictionary of query parameters to include in the request. Defaults to None.
            _parent (optional): An optional parent object to associate with the retrieved objects. Defaults to None.

        Returns:
            List[ObjectBase]: A list of objects retrieved from the URL.
        """
        # The object manager has a fixed criteria to execute in all get request?
        if self._fixed_criteria:
            if params:
                params.update(self._fixed_criteria)
            else:
                params = deepcopy(self._fixed_criteria)

        response = self.request.http_get(url, params)

        # If the object manager has a tuple of key response, we'll get
        #   the response recursivally.
        # TODO: Predict a exception for empty response or similar
        if self._key_response is not None:
            for key in self._key_response:
                response = response[key]

        obj_list = []
        for obj_dict in response:
            # Creating a new object using _obj_cls provide in the ObjManager class.
            #    The attrs is obj_dict (based on the server response).
            obj = self._obj_cls(self, obj_dict)

            # Use the received _parent object
            #   **OR**
            # Getting manually (trhought a new get request to server) the parent object
            obj._parent = self._get_parent_obj_if_exist(obj, _parent)

            # Update object in our internal cache
            self._update_cache(obj)

            obj_list.append(obj)

        return obj_list

    def get_all(self, _parent: ObjectBase = None) -> List[ObjectBase]:
        """Retrieves all objects from the server for this manager's path.

        Args:
            _parent (ObjectBase, optional): Parent object to associate with retrieved objects. Defaults to None.

        Returns:
            List[ObjectBase]: List of all objects retrieved from the server.
        """
        return self._get(self._path, _parent=_parent)

    def get_by_id(self, id_: Any, use_cache=True, _parent=None) -> ObjectBase:
        """Retrieves an object by its ID from the server or cache.

        Args:
            id_ (Any): The ID of the object to retrieve
            use_cache (bool, optional): Whether to check the cache before making a server request. Defaults to True.
            _parent (ObjectBase, optional): Parent object to associate with the retrieved object. Defaults to None.

        Returns:
            ObjectBase: The object with the specified ID

        Notes:
            - If use_cache is True, first checks internal cache for object
            - If object found in cache and _parent provided, sets parent reference
            - If not found in cache or use_cache is False, makes request to server
        """
        if use_cache:
            obj = self._get_object_from_cache(id_)
            if obj:
                if _parent and not obj._parent:
                    obj._parent = _parent
                return obj

        return self._get(f'{self._path}/{id_}', _parent=_parent)[0]


class GetByCriteriaMixins(GetMixins):
    def get_by_crit(self, crit: dict[str, Any], _parent=None) -> List[ObjectBase]:
        """Get objects matching specified criteria from the Mantis server.

        Args:
            crit (dict[str, Any]): Dictionary of criteria to filter objects by
            _parent (ObjectBase, optional): Parent object to associate with retrieved objects. Defaults to None.

        Returns:
            List[ObjectBase]: List of objects matching the specified criteria
        """
        return self._get(self._path, crit, _parent)


class ManagerBaseMixins(GetMixins):
    ...
