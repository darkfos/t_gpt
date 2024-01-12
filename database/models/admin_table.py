from database.create_all_table import Base
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

class AdminTable(Base):
    __tablename__ = "AdminTable"

    admin_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    tg_name: Mapped[str]
    password: Mapped[str]

    def __init__(self, tg_id: int, tg_name: Mapped[str], password: Mapped[str]):
        self.tg_id = tg_id
        self.tg_name = tg_name
        self.password = password

    def __repr__(self):
        return f"{self.tg_name}, {self.tg_id}, {self.password}"