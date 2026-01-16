from db import db
from bson import ObjectId


class AdminModel:
    COLLECTION = "admins"  

    @staticmethod
    def find_by_username(username: str):
        return db[AdminModel.COLLECTION].find_one(
            {"userName": username}
        )
    
    @staticmethod
    def find_by_id(admin_id: ObjectId):
        return db[AdminModel.COLLECTION].find_one(
            {"_id": admin_id}
        )

    @staticmethod
    def is_password_correct(admin_doc: dict, password: str) -> bool:
        if not admin_doc:
            return False
        return admin_doc.get("password") == password
