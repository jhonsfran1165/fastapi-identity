from typing import Any, Dict, Optional, Union

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from loguru import logger

from app.core.security import get_password_hash, verify_password
from app.core.crud.base import CRUDBase
from app.user.models.user import User, UserCreate, UserUpdate


@logger.catch
class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        results = await db.exec(statement)
        return results.first()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
            is_verified=obj_in.is_verified
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(db, email=email)

        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_verified(self, user: User) -> bool:
        return user.is_verified

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

user = CRUDUser(User)
