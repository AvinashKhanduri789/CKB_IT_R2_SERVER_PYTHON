from db import db
from datetime import datetime, timezone


class QuestionModel:
    COLLECTION = "questions"  

    @staticmethod
    def find_all():
        return list(db[QuestionModel.COLLECTION].find())

    @staticmethod
    def find_by_id(question_id):
        return db[QuestionModel.COLLECTION].find_one({"_id": question_id})

    @staticmethod
    def create(text, difficulty="medium", max_score=30, test_cases=None):
        question = {
            "text": text,
            "difficulty": difficulty,
            "maxScore": max_score,
            "testCases": test_cases or [],
            "createdAt": datetime.now(timezone.utc)
        }
        return db[QuestionModel.COLLECTION].insert_one(question)

    @staticmethod
    def update(question_id, data: dict):
        return db[QuestionModel.COLLECTION].update_one(
            {"_id": question_id},
            {"$set": data}
        )

    @staticmethod
    def delete(question_id):
        return db[QuestionModel.COLLECTION].delete_one(
            {"_id": question_id}
        )
