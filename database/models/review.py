from config import SQL_ALCHEMY_URL

from sqlalchemy import BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

#Логирование, подключение
engine = create_async_engine(SQL_ALCHEMY_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str]
    age: Mapped[int]
    review_text: Mapped[str]

    def __init__(self, tg_id, review_text: Mapped[str], name: Mapped[str], age: Mapped[int]):
        self.tg_id = tg_id
        self.review_text = review_text
        self.name = name
        self.age = age

    def __repr__(self):
        return f"tg_id: {self.tg_id}, id_review: {self.id}, name: {self.name}, age: {self.age} review_text: {self.review_text}"


async def create_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)