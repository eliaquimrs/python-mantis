from typing import Any, List

from mantis.base import ObjectManagerBase, ObjectBase


class GetMixins(ObjectManagerBase):
    def _get(
        self,
        url: str,
        params: dict[str, Any] = None,
        _parent=None
    ) -> List[ObjectBase]:

        if self._fixed_criteria:
            if params:
                params.update(self._fixed_criteria)
            else:
                params = self._fixed_criteria

        response = self.request.http_get(url, params)

        if self._key_response is not None:
            for key in self._key_response:
                response = response[key]

        obj_list = []
        for obj_dict in response:
            obj = self._obj_cls(self, obj_dict)
            obj._parent = self._get_parent_obj_if_exist(obj, _parent)

            self._update_cache(obj)

            obj_list.append(obj)

        return obj_list

    def get_all(self, _parent=None) -> List[ObjectBase]:
        return self._get(self._path, _parent=_parent)

    def get_by_id(self, id_: Any, use_cache=True, _parent=None) -> ObjectBase:
        if use_cache:
            obj = self._get_object_from_cache(id_)
            if obj:
                print('Using object from cache')
                if _parent and not obj._parent:
                    obj._parent = _parent
                return obj

            print('obj not found in cache')

        return self._get(f'{self._path}/{id_}', _parent=_parent)[0]


class GetByCriteriaMixins(GetMixins):
    def get_by_crit(self, crit: dict[str, Any], _parent=None) -> List[ObjectBase]:
        return self._get(self._path, crit, _parent)


class ManagerBaseMixins(GetMixins):
    ...
