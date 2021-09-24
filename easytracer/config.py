from easytracer.tracer import Tracer


class ConfigKeys:
    REPORT_HOST = "reporter_host"
    REPORT_PORT = "reporter_port"


class Config:
    def __init__(self, service_name: str, config: dict):
        self.service_name = service_name
        self.logging = config.get("logging", True)
        self.sampler = config.get("sampler", dict()).get("param", 1)
        self.config = config

    def init_tracer(self) -> Tracer:
        return Tracer(self.service_name, self.logging, self.sampler, self.config)
