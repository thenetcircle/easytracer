import os
from pathlib import Path

from fastapi import FastAPI
from gnenv import create_env

from et.common.api import CollectorApi
from et.utils.config import ConfigKeys
from et.utils.custom_logging import CustomizeLogger
from et.utils.decorators import wrap_exception

env = create_env(gn_environment=os.environ.get("ET_ENV", "local"))
api = CollectorApi(env)
app = FastAPI()

# force fastapi/uvicorn to use loguru
config_path = Path(__file__).with_name("logging_config.json")
custom_logger = CustomizeLogger.make_logger(config_path)
app.logger = custom_logger

endpoint = env.config.get(ConfigKeys.UI_BIND, ConfigKeys.DEFAULT_UI_BIND)


@app.get("/v1/event/{event_id}/spans")
@wrap_exception()
async def get_spans(event_id):
    return await api.get(event_id)
