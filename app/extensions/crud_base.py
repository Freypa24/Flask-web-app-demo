from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, Any, Dict, List


class CRUDMixin:
    model = None

    @classmethod
    def get(cls, db: Session, id: Any, id_field: str = "id", *fields: str, ) -> List[Any]:
        stmt = select(cls.model)
        column = getattr(cls.model, id_field)
        return None

    @classmethod
    def get_one(cls, db: Session, id: Any, id_field: str = "id") -> Optional[Any]:
        column = getattr(cls.model, id_field)
        result = db.execute(select(cls.model).where(column == id))
        return result.scalar_one_or_none()

    @classmethod
    def get_by_email(cls, db: Session, email: str) -> Optional[Any]:
        stmt = select(cls.model).where(cls.model.email == email)
        result = db.execute(stmt).scalar_one_or_none()
        return result

    @classmethod
    def get_fields(cls, db: Session, id: Any, *fields: str) -> List[Any]:
        valid_fields = {column.name for column in cls.model.__table__.columns}
        for field in fields:
            if field not in valid_fields:
                raise ValueError(f"Invalid field requested: '{field}'")

        columns = [getattr(cls.model, field) for field in fields]

        stmt = select(*columns).where(cls.model.id == id)
        result = db.execute(stmt).all()
        return result

    @classmethod
    def get_all(cls, db: Session, filters: Dict = None) -> List[Any]:
        stmt = select(cls.model)
        if filters:
            for key, value in filters.items():
                column = getattr(cls.model, key, None)
                if column is not None:
                    stmt = stmt.where(column == value)
        return db.scalars(stmt).all()

    @classmethod
    def create(cls, db: Session, obj_in: Dict[str, Any]) -> Any:
        db_obj = cls.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def update(cls, db: Session, db_obj: Any, obj_in: dict[str, Any]) -> Any:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def delete(cls, db: Session, id: Any) -> Optional[Any]:
        obj = db.get(cls.model, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj