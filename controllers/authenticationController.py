from fastapi import APIRouter, status, Request, Depends
from filters import requestFilter, responseFilter
from services import authenticationService
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/admin/register", response_model=responseFilter.Response, status_code=status.HTTP_201_CREATED)
async def admin_registration(adminData : requestFilter.AdminRegisterFilter, request : Request):
    return await authenticationService.admin_registration(adminData, request)

@router.post('/admin/login')
async def admin_login(login_form: OAuth2PasswordRequestForm = Depends()):
    return await authenticationService.admin_login(login_form)