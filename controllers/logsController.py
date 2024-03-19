from fastapi import APIRouter, status, Response
from filters import responseFilter, requestFilter
from services import logsService

router = APIRouter()

@router.get("/logs", status_code=status.HTTP_200_OK, response_model=responseFilter.Response)
async def get_logs(query : requestFilter.LogQuery):
    return await logsService.get_logs(query)

@router.get("/logs/excel", response_class=Response, status_code=200)
async def get_logs_excel(query : requestFilter.LogQuery):
    return await logsService.get_logs_excel(query)