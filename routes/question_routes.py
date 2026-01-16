from flask import Blueprint
from controllers.question_controller import (
    get_questions,
    submit_answer,
    status_update
)

question_routes = Blueprint("question_routes", __name__)

question_routes.get("/")(get_questions)
question_routes.post("/submit/<questionNumber>")(submit_answer)
question_routes.post("/status/<questionNumber>")(status_update)
