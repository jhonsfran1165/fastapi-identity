from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email
from app.user import cruds
from app.user.models.user import User, UserCreate, UserUpdate


router = APIRouter(
  prefix="/users"
)

# https://medium.com/swlh/quickly-make-an-api-with-auth-3e1e0ca695ef
# TODO
async def common_parameters(
  db: AsyncSession = Depends(deps.get_db),
  skip: int = 0,
  limit: int = Query(default=100, lte=100),
  current_user: User = Depends(deps.get_current_active_superuser)
):
  return {"db": db, "skip": skip, "limit": limit, "current_user": current_user}



@router.get("/", response_model=List[User])
async def read_users(
  db: AsyncSession = Depends(deps.get_db),
  skip: int = 0,
  limit: int = Query(default=100, lte=100),
  current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
  """
  Retrieve users.
  """
  users = await cruds.user.get_multi(db, skip=skip, limit=limit)
  return users


@router.post("/", response_model=User)
async def create_user(
  *,
  db: AsyncSession = Depends(deps.get_db),
  user_in: UserCreate,
  current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
  """
  Create new user.
  """
  user = await cruds.user.get_by_email(db, email=user_in.email)
  if user:
      raise HTTPException(
          status_code=400,
          detail="The user with this username already exists in the system.",
      )
  user = await cruds.user.create(db, obj_in=user_in)
  if settings.EMAILS_ENABLED and user_in.email:
      send_new_account_email(
          email_to=user_in.email, username=user_in.email, password=user_in.password
      )
  return user


@router.put("/me", response_model=User)
async def update_user_me(
  *,
  db: AsyncSession = Depends(deps.get_db),
  password: str = Body(None),
  full_name: str = Body(None),
  email: EmailStr = Body(None),
  current_user: User = Depends(deps.get_current_active_user),
) -> Any:
  """
  Update own user.
  """
  current_user_data = jsonable_encoder(current_user)
  user_in = UserUpdate(**current_user_data)
  if password is not None:
      user_in.password = password
  if full_name is not None:
      user_in.full_name = full_name
  if email is not None:
      user_in.email = email
  user = await cruds.user.update(db, db_obj=current_user, obj_in=user_in)
  return user


@router.get("/me", response_model=User)
def read_user_me(
  current_user: User = Depends(deps.get_current_active_user),
) -> Any:
  """
  Get current user.
  """
  return current_user


@router.post("/open", response_model=User)
async def create_user_open(
  *,
  db: AsyncSession = Depends(deps.get_db),
  password: str = Body(...),
  email: EmailStr = Body(...),
  full_name: str = Body(None),
) -> Any:
  """
  Create new user without the need to be logged in.
  """

  if not settings.USERS_OPEN_REGISTRATION:
      raise HTTPException(
          status_code=403,
          detail="Open user registration is forbidden on this server",
      )
  user = await cruds.user.get_by_email(db, email=email)
  if user:
      raise HTTPException(
          status_code=400,
          detail="The user with this username already exists in the system",
      )
  user_in = UserCreate(password=password, email=email, full_name=full_name)
  user = await cruds.user.create(db, obj_in=user_in)
  return user


@router.get("/{user_id}", response_model=User)
async def read_user_by_id(
  user_id: int,
  current_user: User = Depends(deps.get_current_active_user),
  db: AsyncSession = Depends(deps.get_db),
) -> Any:
  """
  Get a specific user by id.
  """
  user = await cruds.user.get(db, id=user_id)
  if user == current_user:
      return user
  if not cruds.user.is_superuser(current_user):
      raise HTTPException(
          status_code=400, detail="The user doesn't have enough privileges"
      )
  return user


@router.put("/{user_id}", response_model=User)
async def update_user(
  *,
  db: AsyncSession = Depends(deps.get_db),
  user_id: int,
  user_in: UserUpdate,
  current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
  """
  Update a user.
  """
  user = await cruds.user.get(db, id=user_id)
  if not user:
      raise HTTPException(
          status_code=404,
          detail="The user with this username does not exist in the system",
      )
  user = await cruds.user.update(db, db_obj=user, obj_in=user_in)
  return user
