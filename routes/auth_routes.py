from flask import Blueprint
from controllers.auth_controller import login, logout

auth_routes = Blueprint("auth_routes", __name__)

auth_routes.post("/login")(login)
auth_routes.get("/logout")(logout)
