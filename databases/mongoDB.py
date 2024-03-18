from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL")
DATABASE = os.getenv("DATABASE")

class MongoUtil:
    def __init__(self):
        self._connection = MongoClient(MONGO_URL)
        self._db = self._connection[DATABASE]
        self._studentsCollection = self._db.students
        self._logsCollection = self._db.logs

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