from sqlalchemy import select, insert, delete
from database import create_db, async_session, Review


async def get_all_reviews() -> tuple:
    async with async_session() as session:
        data_result = await session.execute(select(Review))
        all_reviews = data_result.scalars().all()
        return all_reviews
