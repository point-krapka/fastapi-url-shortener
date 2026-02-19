# infrastructure/db/repo/user.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.infrastructure.db.models.user import User
from sqlalchemy.exc import IntegrityError
from app.infrastructure.error import NotFoundError,AlreadyExistsError
async def create_user(db: AsyncSession, user:User) -> User | None:
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError:
        raise AlreadyExistsError("Логін вже зайнятий", "login_taken")

async def delete_user(db: AsyncSession, user_id: int) -> None:
    result = await db.execute(delete(User).where(User.id == user_id))
    await db.commit()
    if result.rowcount == 0:
        raise NotFoundError("Користувач не знайден","user_not_found")

async def get_password_by_login(db: AsyncSession, login: str) -> str | None:
    result = await db.execute(select(User.password).where(User.login == login))
    
    user= result.scalar_one_or_none()
    if user is None:
        raise NotFoundError(message="Користувача не знайдено", reason="user_not_found")
    return user

async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    user =  result.scalar_one_or_none()
    if user is None:
        raise NotFoundError(message="Користувача не знайдено", reason="user_not_found")
    return user

async def get_user_by_login(db: AsyncSession, login: str) -> User | None:
    result = await db.execute(select(User).where(User.login == login))
    user =  result.scalar_one_or_none()
    if user is None:
        raise NotFoundError(message="Користувача не знайдено", reason="user_not_found")
    return user