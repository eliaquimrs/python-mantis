from mantis.base import ObjectManagerBase, ObjectBase
from mantis.mixins import (
    ManagerBaseMixins, GetByCriteriaMixins
)


class NoteObj(ObjectBase):
    _repr_attrs = ['id', '{reporter[name]}']


class NoteManager(
    ManagerBaseMixins,
    GetByCriteriaMixins,
    ObjectManagerBase
):
    _path = 'issues'
    _id_attr = 'id'
    _key_response = ('issues', 0, 'notes')

    # TODO: Review mandatory and optional attributes
    _mandatory_attr = ('id', 'text')
    _optional_attr = ('reporter', 'view_state', 'attachments', 'type',
                      'created_at', 'updated_at')

    _readonly_attr = tuple()

    _obj_cls = NoteObj
    _parent_id_attr = 'id'

    _fixed_criteria = {
        'select': 'notes'
    }
