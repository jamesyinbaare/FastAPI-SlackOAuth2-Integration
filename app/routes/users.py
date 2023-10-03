import os

import aiohttp
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Query
from slack_sdk.web.async_client import AsyncWebClient

from app.schemas import GetUsersPageReq, GetUsersPageRes

load_dotenv()


SLACK_ACCESS_TOKEN = os.getenv("SLACK_ACCESS_TOKEN")
client = AsyncWebClient(token=SLACK_ACCESS_TOKEN)

user_router = APIRouter(tags=["Users"])


@user_router.get("", tags=["users"], response_model=GetUsersPageRes)
async def get_users_page(req: GetUsersPageReq):
    try:
        response = await get_users(req.page_token)
        res = {"page_token": req.page_token, "users": response}
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_users(page_token: str = Query(None)):
    async with aiohttp.ClientSession() as session:
        url = "https://slack.com/api/users.list"
        headers = {"Authorization": f"Bearer {SLACK_ACCESS_TOKEN}"}
        params = {"cursor": page_token}

        async with session.get(url, headers=headers, params=params) as response:
            if response.status != 200:
                raise HTTPException(status_code=500, detail="Slack API error")

            data = await response.json()
            return data
