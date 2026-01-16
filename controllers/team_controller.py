from flask import request, jsonify
from models.team import TeamModel


def create_team():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"message": "Team name is required"}), 400

    try:
        existing_team = TeamModel.find_by_name(name)
        if existing_team:
            return jsonify({"message": "Team name already exists"}), 400

        TeamModel.create(name)

        return jsonify({"name": name}), 201

    except Exception:
        return jsonify({"message": "Server error"}), 500
