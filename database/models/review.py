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

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    review_number: Mapped[int]