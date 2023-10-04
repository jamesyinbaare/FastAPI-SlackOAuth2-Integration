# Armoz Slack OAuth2 integration

This is simple FastAPI that integrates Slack's OAuth2 for user authentication and authorization

## How to run development
1. Rename the .env.sample file to .env and add slack app client_id and client_secret

2. Create and activate virtualenv and run `pip install requirements.dev.txt`
or Run `poetry init` and `poetry install --with dev`

3. Run `docker-compose up -d --build`
