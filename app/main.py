from __future__ import annotations

from fastapi import FastAPI

from .routes import auth

app = FastAPI()

app.include_router(auth.auth_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
