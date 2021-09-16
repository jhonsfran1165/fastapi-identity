from sqlmodel.ext.asyncio.session import AsyncSession

from app.user import cruds
from app.user.models.user import UserCreate
from app.core.config import settings
from app.db import base, session  # noqa: F401


async def init_db(db: AsyncSession) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # session.init_db()

    user = await cruds.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            full_name="Admin User"
        )
        user = await cruds.user.create(db, obj_in=user_in)  # noqa: F841
