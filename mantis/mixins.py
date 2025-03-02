from __future__ import annotations
from mantis.base import TObjManagerClass, ObjectManagerBase


class ListMixins(ObjectManagerBase):
    def list(self):
        response = self.request.http_get(self._path)

        if self._key_response is not None:
            response = response[self._key_response]

        # if self._manage_parent

        obj_list = []
        for obj in response:
            obj_list.append(self._obj_cls(self, obj))

        return obj_list


class ManagerBaseMixins(ListMixins):
    ...
