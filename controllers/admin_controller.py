from flask import jsonify, request
from models.team import TeamModel
from models.question import QuestionModel
from bson import ObjectId



def serialize(obj):
    if isinstance(obj, list):
        return [serialize(item) for item in obj]

    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}

    if isinstance(obj, ObjectId):
        return str(obj)

    return obj


def get_teams():
    try:
        teams = TeamModel.find_all()
        response = []

        for team in teams:
            total_score = (
                team.get("scoreQuestion1", 0)
                + team.get("scoreQuestion2", 0)
                + team.get("scoreQuestion3", 0)
            )

            times = [t for t in team.get("timeTaken", {}).values() if t]
            total_time = None

            if len(times) >= 2:
                sorted_times = sorted([t.timestamp() for t in times])
                total_time = sorted_times[-1] - sorted_times[0]

            response.append({
                "teamName": team.get("name"),
                "totalScore": total_score,
                "totalTime": total_time,
                "timeStamps": team.get("timeTaken"),
                "code": team.get("code"),
                "testCaseResults": team.get("questionResults")
            })

        response.sort(
            key=lambda x: (
                -x["totalScore"],
                float("inf") if x["totalTime"] is None else x["totalTime"]
            )
        )

        return jsonify(response), 200

    except Exception:
        return jsonify({"message": "Server error"}), 500


def create_question():
    data = request.get_json()
    text = data.get("text")
    difficulty = data.get("difficulty")
    max_score = data.get("maxScore")
    test_cases = data.get("testCases")

    if not text or not test_cases:
        return jsonify({"message": "Missing required fields"}), 400

    result = QuestionModel.create(
        text=text,
        difficulty=difficulty,
        max_score=max_score,
        test_cases=test_cases
    )

    question = QuestionModel.find_by_id(result.inserted_id)

    return jsonify({
        "message": "Question created successfully",
        "question": serialize(question)
    }), 201


def update_question(id):
    data = request.get_json()

    updated = QuestionModel.update(
        ObjectId(id),
        {
            "text": data.get("text"),
            "difficulty": data.get("difficulty"),
            "maxScore": data.get("maxScore"),
            "testCases": data.get("testCases")
        }
    )

    if updated.matched_count == 0:
        return jsonify({"message": "Question not found"}), 404

    question = QuestionModel.find_by_id(ObjectId(id))

    return jsonify({
        "message": "Question updated successfully",
        "question": serialize(question)
    }), 200


def delete_question(id):
    deleted = QuestionModel.delete(ObjectId(id))

    if deleted.deleted_count == 0:
        return jsonify({"message": "Question not found"}), 404

    return jsonify({"message": "Question deleted successfully"}), 200
