from fastapi import APIRouter, status
from filters.requestFilter import RegisterFilter, RFIDRegister
from services import studentRegistrationService
from filters import responseFilter

router = APIRouter()

# @router.post('/register')
@router.post('/student/register', status_code=status.HTTP_201_CREATED, response_model=responseFilter.Response)
async def registerUser(student : RegisterFilter):
    return await studentRegistrationService.registerUser(student)

@router.put('/rfid/register', status_code=status.HTTP_200_OK, response_model=responseFilter.Response)
async def registerRfid(rfid : RFIDRegister):
    return await studentRegistrationService.registerRfid(rfid)