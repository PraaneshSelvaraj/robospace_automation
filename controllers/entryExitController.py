from fastapi import APIRouter, status
from filters.requestFilter import Entry, Exit
from filters import responseFilter
from services import entryExitService

router = APIRouter()

@router.post("/entry", status_code=status.HTTP_200_OK, response_model=responseFilter.Response)
async def entry(data : Entry):
    return await entryExitService.entry(data)

@router.post("/exit", status_code=status.HTTP_200_OK, response_model=responseFilter.Response)
async def exitOut(data : Exit):
    return await entryExitService.exitOut(data)

