"""Sub object:
    - attachment.py
    - note.py
"""
from mantis.base import ObjectBase, ObjectManagerBase
from mantis.mixins import (
    ManagerBaseMixins,
    GetByCriteriaMixins
)
from .note import NoteManager


class IssueObj(ObjectBase):
    _repr_attrs = ['id', 'summary']

    def get_notes(self):
        return self.manager._child_manager_obj.get_by_crit({'id': self.id}, self)


class IssueManager(
        ManagerBaseMixins,
        GetByCriteriaMixins,
        ObjectManagerBase):
    _path = 'issues'
    _id_attr = 'id'
    _key_response = ('issues', )

    # TODO: Review mandatory and optional attributes
    _mandatory_attr = (
        'id', 'summary', 'description', 'project', 'steps_to_reproduce')
    _optional_attr = ('category', 'reporter', 'handler', 'status', 'resolution',
                      'view_state', 'priority', 'severity', 'reproducibility',
                      'platform', 'sticky', 'created_at', 'updated_at',
                      'custom_fields', 'history')

    _readonly_attr = tuple()

    _obj_cls = IssueObj
    _parent_id_attr = 'id'

    _child_manager_cls = NoteManager

    _fixed_criteria = {
        'select': ('id,summary,description,project,steps_to_reproduce,category,'
                   'reporter,handler,status,resolution,view_state,priority,'
                   'severity,reproducibility,platform,sticky,created_at,'
                   'updated_at,custom_fields,history')
    }
