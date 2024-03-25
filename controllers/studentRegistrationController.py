from fastapi import APIRouter, status, Depends
from filters.requestFilter import RegisterFilter, RFIDRegister
from services import studentRegistrationService
from filters import responseFilter
from utils import authentication

router = APIRouter()

# @router.post('/register')
@router.post('/student/register', status_code=status.HTTP_201_CREATED, response_model=responseFilter.Response)
async def registerUser(student : RegisterFilter,  token: str = Depends(authentication.oauth2_scheme)):
    return await studentRegistrationService.registerUser(student, token)

@router.put('/rfid/register', status_code=status.HTTP_200_OK, response_model=responseFilter.Response)
async def registerRfid(rfid : RFIDRegister,  token: str = Depends(authentication.oauth2_scheme)):
    return await studentRegistrationService.registerRfid(rfid, token)