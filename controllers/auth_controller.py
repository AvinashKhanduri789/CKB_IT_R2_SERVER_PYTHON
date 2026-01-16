from flask import request, jsonify
import jwt
from datetime import datetime, timedelta, timezone

from models.admin import AdminModel
from config import Config


def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "message": "username and password required"
        }), 400

    admin = AdminModel.find_by_username(username)

    if not admin:
        return jsonify({
            "message": "Could't found any account"
        }), 404

    if not AdminModel.is_password_correct(admin, password):
        return jsonify({
            "message": "Bad Credentials"
        }), 401

    payload = {
        "id": str(admin["_id"]),
        "exp": datetime.now(timezone.utc) + timedelta(days=1)
    }

    access_token = jwt.encode(
        payload,
        Config.JWT_SECRET,
        algorithm="HS256"
    )

    response = jsonify({
        "message": "Loged in successfull",
        "accessToken": access_token
    })

    response.set_cookie(
        "accessToken",
        access_token,
        httponly=True,
        secure=True,      
        samesite="None"   
    )
    print("user loged in sucessfully generated token is",access_token)
    return response, 200


def logout():
    response = jsonify({
        "message": "Logged out successfully"
    })

    response.set_cookie(
        "accessToken",
        "",
        expires=0,
        httponly=True,
        secure=False,
        samesite="Lax"
    )

    return response, 200
