from filters.requestFilter import Entry, Exit
from fastapi.responses import JSONResponse
from fastapi import status, Depends
from databases import mongoDB
from utils import dateTimeUtil, authentication, jwtUtil
import config

mongoUtil = mongoDB.MongoUtil()

async def entry(data : Entry, token: str = Depends(authentication.oauth2_scheme)):
    jwtData = jwtUtil.get_jwt_data(token)
    adminUser = mongoUtil.getAdmin(username=jwtData['user'])
    if adminUser is None:
        return JSONResponse(content={"message" : "Not Authorized.", "data" : ""}, status_code=status.HTTP_401_UNAUTHORIZED)

    if adminUser['admin_type'] != 'device':
        return JSONResponse(content={"message" : "Not Authorized. Must be a device", "data" : ""}, status_code=status.HTTP_401_UNAUTHORIZED)

    if data.rfid is None and data.register_no is None:
        return JSONResponse(content={"message" : "'rfid' or 'register_no' must be provided.", "data" : ""}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    student = None

    if data.rfid:
        student = mongoUtil.getStudent(rfid=data.rfid)
    elif data.register_no:
        student = mongoUtil.getStudent(register_no=data.register_no)

    if student is None:
        return JSONResponse(content={"message" : f"Unable to find student", "data" : {}}, status_code=status.HTTP_404_NOT_FOUND)
    
    entryData = {}
    entryData['register_no'] = student['register_no']

    current_time = dateTimeUtil.get_current_ist_time()
    if config.entry_start_time <= current_time.time() <= config.entry_end_time:
        entryData['datetime'] = current_time
        entryData['state'] = 'entry'
        mongoUtil.entryLog(entryData)
        return {"message" : "Validation successfull"}
    
    else:
        if student['completeAccess'] == True:
            entryData['datetime'] = current_time
            entryData['state'] = 'entry'
            entryData['completeAccess'] = True
            mongoUtil.entryLog(entryData)
            return {"message" : "Validation successfull"}

        else:
            return JSONResponse(content={'message' : "Access Denied", "data" : {}}, status_code=status.HTTP_403_FORBIDDEN)
        
async def exitOut(data : Exit, token: str = Depends(authentication.oauth2_scheme)):
    jwtData = jwtUtil.get_jwt_data(token)
    adminUser = mongoUtil.getAdmin(username=jwtData['user'])
    if adminUser is None:
        return JSONResponse(content={"message" : "Not Authorized.", "data" : ""}, status_code=status.HTTP_401_UNAUTHORIZED)

    if adminUser['admin_type'] != 'device':
        return JSONResponse(content={"message" : "Not Authorized. Must be a device", "data" : ""}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    if data.rfid is None and data.register_no is None:
        return JSONResponse(content={"message" : "'rfid' or 'register_no' must be provided.", "data" : ""}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    student = None

    if data.rfid:
        student = mongoUtil.getStudent(rfid=data.rfid)
    elif data.register_no:
        student = mongoUtil.getStudent(register_no=data.register_no)

    if student is None:
        return JSONResponse(content={"message" : f"Unable to find student", "data" : {}}, status_code=status.HTTP_404_NOT_FOUND)
    
    entryData = {}
    entryData['register_no'] = student['register_no']
    entryData['datetime'] = dateTimeUtil.get_current_ist_time()
    entryData['state'] = 'exit'
    mongoUtil.entryLog(entryData)

    return {"message" : "Validation successfull"}