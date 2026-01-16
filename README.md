# CKB IT R2 Backend

Flask-based backend for a competitive programming platform used in live university events.

## Features
- JWT-based admin authentication (cookie-based)
- Question creation, update, and deletion
- Team management and score tracking
- Code execution and evaluation using the Piston API
- MongoDB integration with a production-ready structure
- CORS-safe setup for frontend integration

## Tech Stack
- Flask
- MongoDB (PyMongo)
- JWT Authentication
- Piston API
- Gunicorn (production server)

## Environment Variables
```bash

MONGO_URI="your mongo uri"
JWT_SECRET="your jwt seceret key"
PISTON_API_URL="Piston url"
PROD=true
```

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```
## Production
Deployed using **Gunicorn** on Render.

