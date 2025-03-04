"""Sub object:
    - issue.py"""

from mantis.base import ObjectBase, ObjectManagerBase
from mantis.mixins import ManagerBaseMixins
from mantis.api.v1.objects.issue import IssueManager


class ProjectObj(ObjectBase):
    _repr_attrs = ('id', 'name', 'enabled')

    @property
    def issue_manager(self):
        return self.manager._child_manager_obj

    def get_issues(self):
        return self.manager._child_manager_obj.get_by_crit(
            {'project_id': self.id}, _parent=self)


class ProjectManager(
    ManagerBaseMixins,
    ObjectManagerBase
):
    _path = 'projects'
    _id_attr = 'id'
    _key_response = ('projects', )
    _mandatory_attr = ('id', 'name', 'enabled')
    _optional_attr = (
        'status', 'description', 'view_state', 'categories', 'inherit_global',
        'access_level',  'custom_fields', 'versions', 'categories'
    )
    _readonly_attr = ('id',)

    _obj_cls = ProjectObj
    _child_manager_cls = IssueManager
