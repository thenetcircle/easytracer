from easytracer.tracer import Tracer


class ConfigKeys:
    AGENT_SOCKET = "agent_socket"
    LOGGING = "logging"
    SAMPLER = "sampler"
    PARAM = "param"


class Config:
    def __init__(self, service_name: str, config: dict):
        self.service_name = service_name
        self.logging = config.get(ConfigKeys.LOGGING, True)
        self.sampler = config.get(ConfigKeys.SAMPLER, dict()).get(ConfigKeys.PARAM, 1)
        self.config = config

    def init_tracer(self) -> Tracer:
        return Tracer(self.service_name, self.logging, self.sampler, self.config)
