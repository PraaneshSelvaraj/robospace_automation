from filters.requestFilter import RegisterFilter, RFIDRegister
from databases import mongoDB
from fastapi.responses import JSONResponse
from utils import dateTimeUtil
from fastapi import status

mongoUtil = mongoDB.MongoUtil()

async def registerUser(student : RegisterFilter):
    existingStudent = mongoUtil.getStudent(student.register_no)
    if existingStudent:
        return JSONResponse(content={"message" : f"Student with register: {student.register_no} already exists.", "data" : {}},status_code=status.HTTP_409_CONFLICT)
    
    student = student.model_dump()
    student['registered_at'] = dateTimeUtil.get_current_ist_time()
    student['rfid'] = ""

    mongoUtil.addStudent(student)
    return {"message" : f"{student['register_no']} registered successfully."}

async def registerRfid(rfid : RFIDRegister):
    student = mongoUtil.getStudent(rfid.register_no)
    if student is None:
        return JSONResponse(content={"message" : f"Unable to find student {rfid.register_no}", "data" : {}}, status_code=status.HTTP_404_NOT_FOUND)
    
    mongoUtil.updateRFID(rfid.register_no, rfid.rfid)
    return {"message" : f"RFID registered successfully for {rfid.register_no}"}