from __future__ import annotations
from mantis.base import TObjManagerClass, ObjectManagerBase


class ListMixins(ObjectManagerBase):
    def list(self):
        response = self.request.http_get(self._path)
        json_response = response.json()

        if self._key_response is not None:
            json_response = json_response[self._key_response]

        # if self._manage_parent

        obj_list = []
        for obj in json_response:
            obj_list.append(self._obj_cls(self, obj))
            break

        return obj_list


class ManagerBaseMixins(ListMixins):
    ...
