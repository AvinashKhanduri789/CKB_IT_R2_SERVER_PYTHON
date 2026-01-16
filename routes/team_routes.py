from flask import Blueprint
from controllers.team_controller import create_team

team_routes = Blueprint("team_routes", __name__)

team_routes.post("/")(create_team)
