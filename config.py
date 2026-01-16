import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_SECRET = os.getenv("JWT_SECRET")
    PISTON_API_URL = os.getenv("PISTON_API_URL")
    PROD = os.getenv("PROD", "false").lower() == "true"
