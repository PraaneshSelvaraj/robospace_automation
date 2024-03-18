from pydantic import BaseModel, validator

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