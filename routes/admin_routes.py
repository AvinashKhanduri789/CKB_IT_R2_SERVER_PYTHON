from flask import Blueprint
from controllers.admin_controller import (
    get_teams,
    create_question,
    update_question,
    delete_question
)
from middleware.with_jwt import with_jwt

admin_routes = Blueprint("admin_routes", __name__)

admin_routes.get("/getTeams")(with_jwt(get_teams))
admin_routes.post("/create")(with_jwt(create_question))
admin_routes.put("/update/<id>")(with_jwt(update_question))
admin_routes.delete("/delete/<id>")(with_jwt(delete_question))