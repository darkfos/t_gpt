from sqlalchemy import select, insert, delete, BigInteger
from database.create_all_table import async_session
from database import AdminTable


async def get_one_admin(tg_id: BigInteger):
    async with async_session as session:
        data_result = await session.execute(select(AdminTable).where(AdminTable.tg_id==tg_id))
        info_about_admin = data_result.all()
        return info_about_admin


async def get_all_admins():
    async with async_session as session:
        data_result = await session.execute(select(AdminTable))
        all_admins = data_result.scalars().all()
        return all_admins


async def add_admin(*args):
    async with async_session as session:
        add_admin_to_table = await session.execute(insert(AdminTable).values(args))
        await session.commit()


async def del_admin(tg_id: BigInteger):
    async with async_session as session:
        del_to_admin = await session.execute(delete(AdminTable).where(AdminTable.tg_id==tg_id))
        await session.commit()