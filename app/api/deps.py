from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi_permissions import Everyone, Authenticated, configure_permissions

from app.user import cruds
from app.user.models.token import TokenPayload
from app.user.models.user import User
from app.core import security
from app.core.config import settings
from app.db.session import get_session

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}/login/access-token"
)


async def get_db():
    async_session = await get_session()
    async with async_session() as db:
        yield db


async def get_token_payload(
    request: Request,
    token: str = Depends(reusable_oauth2)
) -> TokenPayload:
    try:
        # token = request.headers.get('Authorization')
        print(request.headers)
        # ! we are assuming that there is an API gateway whos validate the token
        unverified_payload = jwt.get_unverified_claims(token)
        token_data = TokenPayload(**unverified_payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    return token_data


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = await cruds.user.get(db, id=token_data.sub)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_principals(
    current_user: User = Depends(get_current_user)
) -> dict:
    """ returns the principals of the current logged in user"""

    principals = [Everyone]

    if cruds.user.is_active(current_user):
        # TODO
        principals = [Everyone, Authenticated]

    return principals


# Permission is already wrapped in Depends()
Permission = configure_permissions(get_principals)

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not cruds.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not cruds.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
