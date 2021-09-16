from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.base import BaseTable

ModelType = TypeVar("ModelType", bound=BaseTable)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        # return db.query(self.model).filter(self.model.id == id).first()
        return await db.get(self.model, id)


    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        statement = select(self.model).offset(skip).limit(limit)
        result = await db.exec(statement)
        return result.all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        # TODO: review this
        # .from_orm(hero)
        # obj_in_data = jsonable_encoder(obj_in)
        # db_obj = self.model.from_orm(obj_in)(**obj_in_data)  # type: ignore
        db_obj = self.model.from_orm(obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        # obj = db.query(self.model).get(id)
        obj = db.get(self.model, id)
        db.delete(obj)
        db.commit()
        return obj
