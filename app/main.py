from __future__ import annotations

from fastapi import FastAPI

from .routes import auth, events, users

app = FastAPI()

app.include_router(auth.auth_router)
app.include_router(users.user_router, prefix="/users")
app.include_router(events.event_router, prefix="/events")


@app.get("/")
async def root():
    return {"message": "Armoz Slack Integration"}
