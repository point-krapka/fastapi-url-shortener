
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.user.model import UserRegister, UserResponse
from app.infrastructure.db.models.user import User
from app.infrastructure.db.repo.user import db_create_user,get_user_by_login
from bcrypt import gensalt, hashpw,checkpw
from app.infrastructure.error import NotFoundError,IncorrectPassword
def hash_password(salt, password):
    return hashpw(password.encode(), salt).decode()

async def create_user(db: AsyncSession, data_register: UserRegister) -> UserResponse:
    salt = gensalt()
    user = User(
        login=data_register.login,
        password=hash_password(salt, data_register.password),
        salt=salt.decode(),
        is_admin=False
    )
    user = await db_create_user(db, user)
    return UserResponse(
        id=user.id,
        login=user.login,
        is_admin=user.is_admin,
        created_at=user.created_at
    )


async def login_user(db: AsyncSession, data: UserRegister) -> UserResponse:
    user = await get_user_by_login(db, data.login)
    if not checkpw(data.password.encode(), user.password.encode()):
        raise IncorrectPassword("Невірний пароль", "incorrect_password")
    return UserResponse(id=user.id, login=user.login, is_admin=user.is_admin, created_at=user.created_at)