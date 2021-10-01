import os
from pathlib import Path

from fastapi import FastAPI
from gnenv import create_env
from loguru import logger

from et.collector.api import CollectorApi
from et.collector.models.event import Event
from et.utils.config import ConfigKeys
from et.utils.custom_logging import CustomizeLogger
from et.utils.decorators import wrap_exception

env = create_env(os.environ.get("ET_ENV", "local"))
api = CollectorApi()
app = FastAPI()

# force fastapi/uvicorn to use loguru
config_path = Path(__file__).with_name("logging_config.json")
custom_logger = CustomizeLogger.make_logger(config_path)
app.logger = custom_logger

endpoint = env.config.get(ConfigKeys.COLLECTOR_ENDPOINT, ConfigKeys.DEFAULT_COLLECTOR_ENDPOINT)
api_path = "/" + endpoint.split("/", 3)[-1]

logger.info(f"listening on api path: {api_path}")


@app.post(api_path)
@wrap_exception()
async def check(event: Event):
    # TODO: what if cassandra is down, back-pressure? retry?
    #  how long? agent queues might fill up, save somewhere temporary?
    return await api.post(event)
