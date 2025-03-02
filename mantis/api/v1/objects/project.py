"""Sub object:
    - issue.py"""

from mantis.base import ObjectBase, ObjectManagerBase
from mantis.mixins import ManagerBaseMixins


class ProjectObj(ObjectBase):
    _repr_attrs = ('name', 'id', 'enabled')


class ProjectManager(
    ManagerBaseMixins,
    ObjectManagerBase
):
    _path = 'projects'
    _id_attr = 'id'
    _key_response = 'projects'
    _mandatory_attr = ('id', 'name', 'enabled')
    _optional_attr = (
        'status', 'description', 'view_state', 'categories', 'inherit_global',
        'access_level',  'custom_fields', 'versions', 'categories'
    )
    _readonly_attr = ('id',)

    _obj_cls = ProjectObj
