from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.visit import Visit


async def save_visit(db: AsyncSession, visit: Visit):
    db.add(visit)
    await db.commit()
    return visit
