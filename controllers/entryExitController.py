from fastapi import APIRouter, status, Depends
from filters.requestFilter import Entry, Exit
from filters import responseFilter
from services import entryExitService
from utils import authentication

router = APIRouter()

@router.post("/entry", status_code=status.HTTP_200_OK, response_model=responseFilter.Response)
async def entry(data : Entry, token: str = Depends(authentication.oauth2_scheme)):
    return await entryExitService.entry(data, token)

@router.post("/exit", status_code=status.HTTP_200_OK, response_model=responseFilter.Response)
async def exitOut(data : Exit, token: str = Depends(authentication.oauth2_scheme)):
    return await entryExitService.exitOut(data, token)

