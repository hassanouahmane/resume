from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from app.api.auth import routes as auth_routes

app = FastAPI(title=os.getenv("APP_NAME", "Resume API"))

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(auth_routes.router)


@app.get("/")
def root():
	return {"status": "ok", "service": "Resume API"}

