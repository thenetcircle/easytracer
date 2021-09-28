import os

from fastapi import FastAPI
from gnenv import create_env
from loguru import logger
from starlette.requests import Request

from etcollector.api import CollectorApi
from utils.config import ConfigKeys

ENVIRONMENT = os.environ.get("ET_ENVIRONMENT", "local")

env = create_env(ENVIRONMENT)
api = CollectorApi()
app = FastAPI()
app.logger = logger

endpoint = env.config.get(ConfigKeys.COLLECTOR_ENDPOINT, ConfigKeys.DEFAULT_COLLECTOR_ENDPOINT)
api_path = endpoint.split("/", 3)[-1]


@app.post(api_path)
async def check(request: Request):  # TODO: use pydantic?
    return await api.post(request)
