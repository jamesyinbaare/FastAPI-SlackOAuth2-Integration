import os
from typing import Optional

from aiohttp import ClientSession
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from slack_sdk.web.async_client import AsyncWebClient

from app.schemas import GetUsersPageReq, GetUsersPageRes

load_dotenv()


SLACK_ACCESS_TOKEN = os.getenv("SLACK_ACCESS_TOKEN")
client = AsyncWebClient(token=SLACK_ACCESS_TOKEN)

user_router = APIRouter(tags=["Users"])


async def get_users(page_token: str):
    async with ClientSession() as session:
        url = "https://slack.com/api/users.list"
        headers = {"Authorization": f"Bearer {SLACK_ACCESS_TOKEN}"}
        params = {"cursor": page_token}

        async with session.get(url, headers=headers, params=params) as response:
            if response.status != 200:
                raise HTTPException(status_code=500, detail="Something went wrong!")

            data = await response.json()
            return data


@user_router.get("", response_model=GetUsersPageRes)
async def get_users_page(req: Optional[GetUsersPageReq] = None):
    if req is None:
        page_token = ""
    else:
        page_token = req.page_token

    try:
        response = await get_users(page_token)
        page_token = response.get("response_metadata")["next_cursor"]
        members = response.get("members")
        users = []
        for member in members:
            org_id = member.get("team_id")
            user_id = member.get("id")
            profile = member.get("profile")
            primary_email = profile.get("email")
            user_email = {
                "address": primary_email,
                "primary": member.get("is_email_confirmed"),
            }
            name = {
                "given_name": profile.get("first_name"),
                "family_name": profile.get("first_name"),
                "full_name": profile.get("display_name"),
            }
            suspended = member.get("is_restricted")
            archived = member.get("is_ultra_restricted")
            is_admin = member.get("is_admin")
            admin_extra_info = {
                "is_admin": member.get("is_admin"),
                "is_owner": member.get("is_owner"),
                "is_primary_owner": member.get("is_primary_owner"),
            }
            user = {
                "org_id": org_id,
                "user_id": user_id,
                "primary_email": primary_email,
                "suspended": suspended,
                "archived": archived,
                "is_admin": is_admin,
                "admin_extra_info": admin_extra_info,
                "name": name,
                "emails": [user_email],
            }
            users.append(user)
        res = {"page_token": page_token, "users": users}
        return res
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@user_router.get("/apps")
async def get_apps_per_user():
    return {"ok": "true", "details": "Not implemented"}


@user_router.get("/run")
async def run():
    async with ClientSession() as session:
        async with session.get("http://localhost:8000/users") as users_res, session.get(
            "http://localhost:8000/users/apps"
        ) as apps_res:
            users_data = await users_res.json()
            apps_data = await apps_res.json()
    return {"users": users_data, "apps": apps_data}
