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
from typing import Any


class IssueObj(ObjectBase):
    _repr_attrs = ['id', 'summary']

    def get_notes(self):
        return self.manager._child_manager_obj.get_by_crit({'id': self.id}, self)
    # TODO: Add method to update issue status
    # TODO: Add method to add/update tags
    # TODO: Add method to monitor/unmonitor issue
    # TODO: Add method to assign issue to user


class IssueManager(
        ManagerBaseMixins,
        GetByCriteriaMixins,
        ObjectManagerBase):
    _path = 'issues'
    _id_attr = 'id'
    _key_response = ('issues', )

    # TODO: Review mandatory, optional and readonly attributes
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

    # TODO: Add function to get issues by project ID/name
    # TODO: Add function to get issues assigned to current user
    # TODO: Add function to get monitored issues (by current user)
    # TODO: Add function to get issues by status (open, closed, resolved etc)
    # TODO: Add function to get issues by priority level
    # TODO: Add function to get issues by severity level
    # TODO: Add function to get issues by category
    # TODO: Add function to get issues created within date range
