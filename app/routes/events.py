import os

import aiofiles
from aiohttp import ClientSession
from dotenv import load_dotenv
from fastapi import APIRouter
from slack_sdk.web.async_client import AsyncWebClient

load_dotenv()


SLACK_ACCESS_TOKEN = os.getenv("SLACK_ACCESS_TOKEN")
SLACK_BOT_ACCESS_TOKEN = os.getenv("SLACK_BOT_ACCESS_TOKEN")
client = AsyncWebClient(token=SLACK_ACCESS_TOKEN)

event_router = APIRouter(tags=["events"])


@event_router.post("")
async def file_events(event: dict):
    challenge = event.get("challenge")

    if "event" in event and event["event"]["type"] == "file_shared":
        file_id = event["event"]["file_id"]
        user_id = event["event"]["user_id"]  # TODO: use user_id to get user_name
        try:
            response = await client.files_info(file=file_id)
            file = response.get("file")
            file_ts = file.get("timestamp")
            file_name = file.get("name")
            file_type = file.get("filetype")
            file_size = file.get("size")
            file_url = file.get("url_private_download")

            file_path = f"{user_id}_{file_ts}_{file_name}"
            await download_file(file_url, file_path)

            print(f"File shared by     : {user_id}")
            print(f"File siz           : {file_size}")
            print(f"File Type          : {file_type}")
            print(f"Shared at          : {file_ts}")
            print(f"File download path : {file_url}")
        except Exception as e:
            print(f"Could not download files: {e}")

    # slack uses the challenge token to verify the event request url
    return challenge


async def download_file(url, save_path):
    headers = {"Authorization": f"Bearer {SLACK_ACCESS_TOKEN}"}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.content.read()
                async with aiofiles.open(save_path, "+wb") as f:
                    await f.write(data)
            else:
                print("File download failed")
