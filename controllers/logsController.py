from fastapi import APIRouter, status, Response, Depends
from filters import responseFilter, requestFilter
from services import logsService
from utils import authentication

router = APIRouter()

@router.get("/logs", status_code=status.HTTP_200_OK, response_model=responseFilter.Response)
async def get_logs(query : requestFilter.LogQuery, token: str = Depends(authentication.oauth2_scheme)):
    return await logsService.get_logs(query, token)

@router.get("/logs/excel", response_class=Response, status_code=200)
async def get_logs_excel(query : requestFilter.LogQuery,  token: str = Depends(authentication.oauth2_scheme)):
    return await logsService.get_logs_excel(query, token)