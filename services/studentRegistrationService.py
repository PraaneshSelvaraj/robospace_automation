from filters.requestFilter import RegisterFilter, RFIDRegister
from databases import mongoDB
from fastapi.responses import JSONResponse
from utils import dateTimeUtil, jwtUtil, authentication
from fastapi import status, Depends

mongoUtil = mongoDB.MongoUtil()

async def registerUser(student : RegisterFilter,  token: str = Depends(authentication.oauth2_scheme)):
    jwtData = jwtUtil.get_jwt_data(token)
    adminUser = mongoUtil.getAdmin(username=jwtData['user'])
    if adminUser is None:
        return JSONResponse(content={"message" : "Not Authorized.", "data" : ""}, status_code=status.HTTP_401_UNAUTHORIZED)

    if adminUser['admin_type'] != 'user':
        return JSONResponse(content={"message" : "Not Authorized. Must be a user", "data" : ""}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    existingStudent = mongoUtil.getStudent(register_no=student.register_no)
    if existingStudent:
        return JSONResponse(content={"message" : f"Student with register: {student.register_no} already exists.", "data" : {}},status_code=status.HTTP_409_CONFLICT)
    
    student = student.model_dump()
    student['registered_at'] = dateTimeUtil.get_current_ist_time()
    student['rfid'] = ""

    mongoUtil.addStudent(student)
    return {"message" : f"{student['register_no']} registered successfully."}

async def registerRfid(rfid : RFIDRegister,  token: str = Depends(authentication.oauth2_scheme)):
    jwtData = jwtUtil.get_jwt_data(token)
    adminUser = mongoUtil.getAdmin(username=jwtData['user'])
    if adminUser is None:
        return JSONResponse(content={"message" : "Not Authorized.", "data" : ""}, status_code=status.HTTP_401_UNAUTHORIZED)

    if adminUser['admin_type'] != 'user':
        return JSONResponse(content={"message" : "Not Authorized. Must be a user", "data" : ""}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    student = mongoUtil.getStudent(register_no=rfid.register_no)
    if student is None:
        return JSONResponse(content={"message" : f"Unable to find student {rfid.register_no}", "data" : {}}, status_code=status.HTTP_404_NOT_FOUND)
    
    mongoUtil.updateRFID(rfid.register_no, rfid.rfid)
    return {"message" : f"RFID registered successfully for {rfid.register_no}"}