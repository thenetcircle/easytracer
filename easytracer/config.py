from easytracer.tracer import Tracer


class Config:
    def __init__(self, service_name: str, config: dict):
        self.service_name = service_name
        self.logging = config.get("logging", True)
        self.sampler = config.get("sampler", dict()).get("param", 1)

    def init_tracer(self) -> Tracer:
        return Tracer(self.service_name, self.logging, self.sampler)
