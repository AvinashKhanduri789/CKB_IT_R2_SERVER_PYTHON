import jwt
from functools import wraps
from flask import request, jsonify, g
from bson import ObjectId

from config import Config
from models.admin import AdminModel


def with_jwt(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        if request.method == "OPTIONS":
            return "", 204

        token = request.cookies.get("accessToken")
        if not token:
            return jsonify({"messege": "Unauthorized request"}), 401

        try:
            decoded = jwt.decode(
                token,
                Config.JWT_SECRET,
                algorithms=["HS256"]
            )
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return jsonify({"messege": "Invalid or expired token"}), 401

        admin_id = decoded.get("id")
        admin = AdminModel.find_by_id(ObjectId(admin_id))
        if not admin:
            return jsonify({"message": "Invalid access token"}), 401

        g.admin = admin
        return fn(*args, **kwargs)

    return wrapper 