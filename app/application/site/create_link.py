import secrets
import string
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.link import Link
from app.infrastructure.error import AlreadyExistsError
from app.infrastructure.db.repo.link import db_create_link
import shortuuid
ALPHABET = string.ascii_letters + string.digits
SHORT_URL_LENGTH = 8



def _generate_short_url() -> str:
    return shortuuid.uuid()[:8]

async def create_link(
    db: AsyncSession,
    origin_url: str,
    user_id: int,
    repeat:int = 5
) -> Link:
    for _ in range(repeat):
        candidate = _generate_short_url()
        link = Link(
        short_url=candidate,
        origin_url=origin_url,
        user_id=user_id,
    )
        try:
            await db_create_link(db,link)
            return link
        except AlreadyExistsError:
            continue
    raise RuntimeError("Unable to generate unique short_url")