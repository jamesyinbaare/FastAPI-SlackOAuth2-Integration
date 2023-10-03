from __future__ import annotations

from fastapi import FastAPI

from .routes import auth, users

app = FastAPI()

app.include_router(auth.auth_router)
app.include_router(users.user_router, prefix="/users")


@app.get("/")
async def root():
    return {"message": "Hello World"}
