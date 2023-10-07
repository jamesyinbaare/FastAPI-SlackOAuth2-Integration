# Slack OAuth2 integration

This is simple FastAPI that integrates Slack's OAuth2 for user authentication and authorization

## How to run development
1. Rename the .env.sample file to .env and add slack app client_id and client_secret

2. Create and activate virtualenv and run `pip install requirements.dev.txt`
or Run `poetry init` and `poetry install --with dev`

3. Run `docker-compose up -d --build`

# Testing
Slack only allows https redirects for it's OAuth redirect endpoint
In testing the application ngrok was used.

1. Authorize endpoint
{BASE_URL}/slack/oauth builds and return slack authorization url using the client_secret, client_id and the necessary scopes

2. Copy and past the url into a browser to authorize the app. This will call the post_authorize endpoint and returns acces_token, id_token and other information about the authorized user

3. Get users page endpoint {BASE_URL}/users return a paginated list of users

4. Get app_per_users {BASE_URL}/users/apps was partially implemented

5. Run enpoint {BASE_URL}/run returns aggregated results from get_app_per_user and get_users page

6. Verify endpoint {BASE_URL}/verify
To test the verify endpoint, pass the access_token as an authorization header to the endpoint.
