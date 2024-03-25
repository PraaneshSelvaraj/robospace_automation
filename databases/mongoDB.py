from pymongo import MongoClient
import os
import pytz

MONGO_URL = os.getenv("MONGO_URL")
DATABASE = os.getenv("DATABASE")

class MongoUtil:
    def __init__(self):
        self._connection = MongoClient(MONGO_URL)
        self._db = self._connection[DATABASE]
        self._studentsCollection = self._db.students
        self._logsCollection = self._db.logs
        self._adminsCollection = self._db.admins

    def getStudent(self,register_no : str = None, rfid : str = None) -> dict:
        try:
            if register_no:
                student = self._studentsCollection.find_one({"register_no" : register_no})
            elif rfid:
                student = self._studentsCollection.find_one({"rfid" : rfid})
                
            student.pop("_id", None)
            return student
        
        except: return None
        
    def addStudent(self, student : dict) -> bool:
        try:
            self._studentsCollection.insert_one(student)
            return True
        
        except: return False

    def updateRFID(self, register_no : str, rfid : str) -> bool:
        try:
            self._studentsCollection.update_one({"register_no" : register_no}, {"$set" : {"rfid" : rfid}})
            return True
        
        except: return False

    def entryLog(self, entryData : dict) -> bool:
        
        try:
            self._logsCollection.insert_one(entryData)
            return True
        
        except: return False

    def get_logs(self, start_date = None, end_date = None) -> list:
        ist_timezone = pytz.timezone('Asia/Kolkata')
        if end_date:
            end_date = end_date.replace(hour=23, minute=59, second=59)

        if start_date is not None and end_date is not None:
            logsResult = self._logsCollection.find({"datetime": {"$gte": start_date, "$lte": end_date}})

        elif start_date is not None:
            logsResult = self._logsCollection.find({"datetime": {"$gte": start_date}})

        elif end_date is not None:
            logsResult = self._logsCollection.find({"datetime": {"$lte": end_date}})

        else:
            logsResult = self._logsCollection.find()
            
        logs = []
        
        for log in logsResult:
            log.pop("_id", None)
            log["datetime"] = log["datetime"].replace(tzinfo=pytz.utc).astimezone(ist_timezone).strftime('%Y-%m-%dT%H:%M:%S.%f')
            logs.append(log)

        return logs
    
    def getAdmin(self, username : str) -> dict:
        try:
            
            student = self._adminsCollection.find_one({"username" : username})
                
            student.pop("_id", None)
            return student
        
        except: return None

    def addAdmin(self, admin : dict) -> bool:
        try:
            self._adminsCollection.insert_one(admin)
            return True
        
        except: return False