from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

from core.models import RequestTable
from .schemas import RequestTableCreate

async def get_all_request_table(session: AsyncSession):
    stmt = select(RequestTable).order_by(RequestTable.id)
    result: Result = await session.execute(stmt)
    return result.scalars().all()

async def get_request_table(session: AsyncSession, request_id: int) -> RequestTable | None:
    return await session.get(RequestTable, request_id)


async def create_request_table(session: AsyncSession, request_in: RequestTableCreate) -> RequestTable | None:
    req = RequestTable(**request_in.model_dump())
    session.add(req)
    await session.commit()
    #return req
