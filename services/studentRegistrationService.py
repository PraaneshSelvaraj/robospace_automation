from filters.requestFilter import RegisterFilter
from databases import mongoDB
from fastapi.responses import JSONResponse
from utils import dateTimeUtil
from fastapi import status

mongoUtil = mongoDB.MongoUtil()

async def registerUser(student : RegisterFilter):
    existingStudent = mongoUtil.getStudent(student.register_no)
    if existingStudent:
        return JSONResponse(content={"message" : f"Student with register: {student.register_no} already exists."},status_code=status.HTTP_409_CONFLICT)
    
    student = student.model_dump()
    student['registered_at'] = dateTimeUtil.get_current_ist_time()
    student['rfid'] = ""

    mongoUtil.addStudent(student)
    return {"message" : f"{student['register_no']} registered successfully."}