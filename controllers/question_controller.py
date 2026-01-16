from flask import request, jsonify
from bson import ObjectId
from datetime import datetime, timezone
import requests

from models.question import QuestionModel
from models.team import TeamModel
from utils.piston import execute_code
from utils.normalize import normalize



def get_questions():
    try:
        questions = QuestionModel.find_all()
        safe_questions = []

        for q in questions:
            safe_questions.append({
                "_id": str(q["_id"]),
                "text": q.get("text"),
                "difficulty": q.get("difficulty"),
                "maxScore": q.get("maxScore"),
                "createdAt": q.get("createdAt"),
                "testCases": [
                    {
                        "input": tc.get("input"),
                        "expectedOutput": tc.get("expectedOutput"),
                        "isPublic": tc.get("isPublic")
                    }
                    for tc in q.get("testCases", [])
                    if tc.get("isPublic")
                ]
            })

        return jsonify(safe_questions), 200

    except Exception as e:
        return jsonify({"message": "Server error"}), 500


def submit_answer(questionNumber):
    data = request.get_json()

    code = data.get("code")
    language = data.get("language")
    team_name = data.get("teamName")
    submission_time = data.get("submissionTime")
    question_id = data.get("questionId")

    try:
        team = TeamModel.find_by_name(team_name)
        question = QuestionModel.find_by_id(ObjectId(question_id))

        if not team:
            return jsonify({"message": "Team not found"}), 404
        if not question:
            return jsonify({"message": "Question not found"}), 404

        question_key = f"question{questionNumber}"

        if team["marksAwarded"].get(question_key):
            return jsonify({
                "message": f"Submission already exists for {question_key}. Resubmission is not allowed."
            }), 409

        test_cases = question.get("testCases", [])
        total_cases = len(test_cases)
        score_per_case = question.get("maxScore") / total_cases

        passed_count = 0
        test_case_results = []

        for index, tc in enumerate(test_cases):
            stdin = tc["input"].replace("\\n", "\n")

            result = execute_code(language, code, stdin)

            raw_actual = result.get("run", {}).get("output", "")
            raw_expected = tc.get("expectedOutput", "")

            actual = normalize(raw_actual)
            expected = normalize(raw_expected)

            passed = actual == expected
            if passed:
                passed_count += 1

            test_case_results.append({
                "index": index + 1,
                "input": tc.get("input"),
                "expectedOutput": tc.get("expectedOutput"),
                "actualOutput": actual,
                "passed": passed,
                "executedAt": datetime.now(timezone.utc)
            })

        score_awarded = int(passed_count * score_per_case)

        update_query = {
            "$set": {
                f"marksAwarded.{question_key}": True,
                f"code.{question_key}": code,
                f"timeTaken.{question_key}": (
                    datetime.fromisoformat(submission_time)
                    if submission_time else datetime.now(timezone.utc)
                ),
                f"questionResults.{question_key}": {
                    "passedCount": passed_count,
                    "totalCases": total_cases,
                    "scoreAwarded": score_awarded,
                    "testCaseResults": test_case_results
                }
            },
            "$inc": {
                f"scoreQuestion{questionNumber}": score_awarded
            }
        }

        TeamModel.update_submission(team_name, update_query)

        return jsonify({
            "message": f"{passed_count}/{total_cases} test cases passed",
            "scoreAdded": score_awarded,
            "details": test_case_results
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Execution error",
            "details": str(e)
        }), 500



def status_update(questionNumber):
    data = request.get_json()

    team_name = data.get("teamName")
    code = data.get("code")
    submission_time = data.get("submissionTime")

    try:
        TeamModel.update_submission(
            team_name,
            {
                "$set": {
                    f"marksAwarded.question{questionNumber}": True,
                    f"timeTaken.question{questionNumber}": (
                        datetime.fromisoformat(submission_time)
                        if submission_time else datetime.now(timezone.utc)
                    ),
                    f"code.question{questionNumber}": code
                }
            }
        )

        return jsonify({"message": "Status updated successfully"}), 200

    except Exception as e:
        return jsonify({
            "message": "Server error during status update",
            "details": str(e)
        }), 500
