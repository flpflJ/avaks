from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .schemas import RequestTableCreate, RequestTable


router = APIRouter(prefix="/rrouter", tags=['rrouter'])


@router.get("/all", response_model=list[RequestTable])
async def get_all_req(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_all_request_table(session=session)


@router.get("/{req_id}", response_model=RequestTable)
async def get_req(req_id: int, session: AsyncSession = Depends(db_helper.session_dependency)):
    req = await crud.get_request_table(session=session, request_id=req_id)
    if req is None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Request {req_id} not found!"
    )
    else:
        return req


@router.post("/", response_model=RequestTable)
async def create_req(req_in: RequestTableCreate, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.create_request_table(request_in=req_in,session=session)
