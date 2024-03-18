from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL")
DATABASE = os.getenv("DATABASE")

class MongoUtil:
    def __init__(self):
        self._connection = MongoClient(MONGO_URL)
        self._db = self._connection[DATABASE]
        self._studentsCollection = self._db.students

    def getStudent(self,register_no : str) -> dict:
        try:
            user = self._studentsCollection.find_one({"register_no" : register_no})
            user.pop("_id", None)
            return user
        
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