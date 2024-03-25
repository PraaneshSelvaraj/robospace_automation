from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class EmptyValidator:
    @validator("*", pre=True)
    def check_empty_string(cls, val):
        if val == "":
            raise ValueError(f"{val} cannot be an empty string")
        return val

class RegisterFilter(BaseModel, EmptyValidator):
    name: str
    department: str
    batch: str
    register_no: str
    roll_no: str
    completeAccess: bool

class RFIDRegister(BaseModel, EmptyValidator):
    register_no : str
    rfid : str

class Entry(BaseModel):
    rfid: Optional[str] = None
    register_no: Optional[str] = None

class Exit(BaseModel):
    rfid: Optional[str] = None
    register_no: Optional[str] = None

class LogQuery(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class AdminRegisterFilter(BaseModel, EmptyValidator):
    username : str
    password : str
    check_password : str
    admin_type : str