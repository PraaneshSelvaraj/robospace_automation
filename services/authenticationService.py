from fastapi import status, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from filters import requestFilter
from databases import mongoDB
from utils import dateTimeUtil, authentication, jwtUtil
import os

mongoUtil = mongoDB.MongoUtil()

async def admin_registration(adminData : requestFilter.AdminRegisterFilter, request: Request):
    headers = request.headers
    
    if "admin-auth-header"not in headers:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message" : "Unauthorized Access.", "data":{}})
    
    if headers['admin-auth-header'] != os.getenv("ADMIN_AUTH_TOKEN"):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message" : "Unauthorized Access.", "data":{}})
        
    if adminData.password != adminData.check_password:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message" : "Password doesn't match", "data":{}})

    if adminData.admin_type not in ['user', 'device']:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message" : "Invalid Admin Type.", "data":{}})

    existingAdmin = mongoUtil.getAdmin(adminData.username)
    if existingAdmin:
        return JSONResponse(content={"message" : f"Username already exists.", "data" : {}},status_code=status.HTTP_409_CONFLICT)
    
    admin = adminData.model_dump()
    admin['registered_at'] = dateTimeUtil.get_current_ist_time()
    admin['password'] = authentication.pwd_context.hash(admin['password'])
    admin.pop('check_password', None)

    mongoUtil.addAdmin(admin)
    return {"message" : "Admin registered successfully."}

async def admin_login(login_form: OAuth2PasswordRequestForm = Depends()):
    admin = mongoUtil.getAdmin(username=login_form.username)
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return JSONResponse(content={"message" : f"Unable to find user", "data" : {}}, status_code=status.HTTP_404_NOT_FOUND)
    
    if not authentication.pwd_context.verify(login_form.password, admin['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    jwtData = {'user' : login_form.username}
    jwtToken = jwtUtil.create_jwt_token(jwtData)

    return {'access_token' : jwtToken, 'token_type' : 'bearer'}
