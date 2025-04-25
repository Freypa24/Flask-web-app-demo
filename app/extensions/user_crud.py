from app.extensions.crud_base import CRUDMixin
from app.models import User

"""
    Assignment of models to conduct CRUD operations must have the liberty to perform custom CRUD operation logics.
    This is for users table.
    Put here custom logic when performing CRUD operations around users table.
    For example, def order_by_age()
"""


class UserCRUD(CRUDMixin):
    model = User
