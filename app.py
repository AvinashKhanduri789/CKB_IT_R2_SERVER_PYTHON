from flask import Flask
from flask_cors import CORS

from routes.team_routes import team_routes
from routes.question_routes import question_routes
from routes.auth_routes import auth_routes
from routes.admin_routes import admin_routes
from config import Config


app = Flask(__name__)


CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:5173","https://ckb-it-r2.vercel.app"]
)


@app.route("/health")
def health():
    return {"status": "ok"}


app.register_blueprint(team_routes, url_prefix="/api/teams")
app.register_blueprint(question_routes, url_prefix="/api/questions")
app.register_blueprint(auth_routes, url_prefix="/api/auth")


app.register_blueprint(
    admin_routes,
    url_prefix="/api/admin"
)



if __name__ == "__main__":
    app.run(debug=not Config.PROD)
