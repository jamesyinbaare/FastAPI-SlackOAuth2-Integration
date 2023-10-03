import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status
from slack_sdk.oauth import OpenIDConnectAuthorizeUrlGenerator, RedirectUriPageRenderer
from slack_sdk.oauth.state_store import FileOAuthStateStore
from slack_sdk.web.async_client import AsyncWebClient
from starlette.responses import JSONResponse

from app.schemas import CallPostAuthorizeRes

load_dotenv()

client_id = os.getenv("SLACK_CLIENT_ID")
client_secret = os.getenv("SLACK_CLIENT_SECRET")
redirect_uri = os.getenv("SLACK_REDIRECT_URI")

scopes = ["openid", "email", "profile"]

state_store = FileOAuthStateStore(expiration_seconds=300)


authorization_url_generator = OpenIDConnectAuthorizeUrlGenerator(
    client_id=client_id,
    scopes=scopes,
    redirect_uri=redirect_uri,
)
redirect_page_renderer = RedirectUriPageRenderer(
    install_path="/slack/oauth",
    redirect_uri_path="/slack/oauth_redirect",
)


auth_router = APIRouter()


@auth_router.get("/slack/oauth", tags=["oauth"])
async def authorize():
    state = state_store.issue()
    url = authorization_url_generator.generate(state=state)
    return {
        "redirect_url": url,
    }


@auth_router.get("/slack/oauth_redirect", response_model=CallPostAuthorizeRes)
async def oauth_callback(code: str, state: str):
    if code is not None:
        if state_store.consume(state):
            try:
                token_response = await AsyncWebClient().openid_connect_token(
                    client_id=client_id, client_secret=client_secret, code=code
                )

                access_token = token_response.get("access_token")
                id_token = token_response.get("id_token")
                state = token_response.get("state")

                user_info_response = await AsyncWebClient(token=access_token).openid_connect_userInfo()

                protected_data = {"access_token": access_token, "id_token": id_token, "state": state}
                consent_usr = user_info_response.get("sub")

                res = {
                    "protected_data": protected_data,
                    "consent_user": consent_usr,
                    "metadata": {**user_info_response.data},
                }
                response = JSONResponse(content=res)
                response.headers["Authorization"] = f"Bearer {access_token}"
                return response

            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Authorization code has expired")

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code")
