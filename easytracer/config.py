from easytracer.tracer import Tracer
from easytracer.config_keys import ConfigKeys


class Config:
    def __init__(self, service_name: str, config: dict):
        self.service_name = service_name
        self.logging = config.get(ConfigKeys.LOGGING, True)
        self.sampler = config.get(ConfigKeys.SAMPLER, dict()).get(ConfigKeys.PARAM, 1)
        self.config = config

    def init_tracer(self) -> Tracer:
        return Tracer(self.service_name, self.logging, self.sampler, self.config)
