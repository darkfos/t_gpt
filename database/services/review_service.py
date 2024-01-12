from sqlalchemy import select, insert, delete, BigInteger
from database.create_all_table import async_session
from database import Review


async def get_all_reviews() -> tuple:
    async with async_session() as session:
        data_result = await session.execute(select(Review))
        all_reviews = data_result.scalars().all()
        return all_reviews


async def get_one_reviews(id_tg: BigInteger) -> tuple:
    async with async_session() as session:
        data_result = await session.execute(select(Review).where(Review.tg_id.is_(id_tg)))
        unique_review = data_result.all()
        return unique_review


async def add_one_reviews(id_tg: BigInteger, name_user: str, age_user: int, review_text: str):
    async with async_session() as session:
        object_to_add: Review = Review(id_tg, review_text, name_user, age_user)
        data_result = session.add(object_to_add)
        await session.commit()


async def del_one_reviews(id_tg: BigInteger):
    async with async_session() as session:
        del_unique_tg_id = await session.execute(delete(Review).where(Review.tg_id == id_tg))
        await session.commit()


