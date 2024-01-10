from sqlalchemy import select, insert, delete, BigInteger
from database import create_db, async_session, Review


async def get_all_reviews() -> tuple:
    async with async_session() as session:
        data_result = await session.execute(select(Review))
        all_reviews = data_result.scalars().all()
        return all_reviews


async def get_one_reviews(id_tg: BigInteger) -> tuple:
    async with async_session() as session:
        data_result = await session.execute(select(Review).where(Review.tg_id.is_(id_tg)))
        unique_review = data_result.scalar_one()
        return unique_review


async def add_one_reviews(id_tg: BigInteger, score_from_user: int):
    async with async_session() as session:
        data_result = await session.add((id_tg, score_from_user))
        session.commit()


async def del_one_reviews(id_tg: BigInteger):
    async with async_session() as session:
        data_result = await session.execute(select(Review).where(Review.tg_id.is_(id_tg)))
        all_reviews_for_unique_id: tuple = data_result.scalars()

        del_results = await session.delete(all_reviews_for_unique_id)
        session.commit()
