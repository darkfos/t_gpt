from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from database.create_all_table import Base

class Review(Base):
    __tablename__ = "ReviewTable"

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