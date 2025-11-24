from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from src.core.cors import setup_cors
from src.routes.router import router

app = FastAPI(title="user-services", version="1.0.0")

setup_cors(app)

app.include_router(router, prefix="/api/v1")
