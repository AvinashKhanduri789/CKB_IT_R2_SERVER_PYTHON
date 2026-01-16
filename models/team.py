from db import db


class TeamModel:
    COLLECTION = "teams"  

    @staticmethod
    def find_all():
        return list(db[TeamModel.COLLECTION].find())

    @staticmethod
    def find_by_name(name: str):
        return db[TeamModel.COLLECTION].find_one({"name": name})

    @staticmethod
    def create(name: str):
        team = {
            "name": name,
            "scoreQuestion1": 0,
            "scoreQuestion2": 0,
            "scoreQuestion3": 0,
            "marksAwarded": {
                "question1": False,
                "question2": False,
                "question3": False,
            },
            "timeTaken": {
                "question1": None,
                "question2": None,
                "question3": None,
            },
            "code": {
                "question1": "",
                "question2": "",
                "question3": "",
            },
            "questionResults": {
                "question1": None,
                "question2": None,
                "question3": None,
            }
        }
        return db[TeamModel.COLLECTION].insert_one(team)

    @staticmethod
    def update_submission(team_name: str, update_query: dict):
        return db[TeamModel.COLLECTION].update_one(
            {"name": team_name},
            update_query
        )
