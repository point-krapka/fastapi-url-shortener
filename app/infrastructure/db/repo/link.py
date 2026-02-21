
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from app.infrastructure.db.models.link import Link
from sqlalchemy.exc import IntegrityError
from app.infrastructure.error import NotFoundError, AlreadyExistsError

async def db_create_link(db: AsyncSession, link: Link) -> Link:
    try:
        db.add(link)
        await db.commit()
        await db.refresh(link)
        return link
    except IntegrityError:
        raise AlreadyExistsError("Посилання вже існує", "link_already_exists")

async def get_link_by_short_url(db: AsyncSession, short_url: str) -> Link:
    result = await db.execute(select(Link).where(Link.short_url == short_url))
    link = result.scalar_one_or_none()
    if link is None:
        raise NotFoundError("Посилання не знайдено", "link_not_found")
    return link

async def get_link_with_visits(db: AsyncSession, short_url: str) -> Link:
    result = await db.execute(
        select(Link)
        .where(Link.short_url == short_url)
        .options(selectinload(Link.visits))
    )
    link = result.scalar_one_or_none()
    if link is None:
        raise NotFoundError("Посилання не знайдено", "link_not_found")
    return link




async def delete_link(db: AsyncSession, link_id: int) -> None:
    result = await db.execute(delete(Link).where(Link.id == link_id))
    await db.commit()
    if result.rowcount == 0:
        raise NotFoundError("Посилання не знайдено", "link_not_found")