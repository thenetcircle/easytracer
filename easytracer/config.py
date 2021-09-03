from easytracer.tracer import Tracer


class Config:
    def __init__(self, config: dict):
        if "service_name" not in config:
            raise AttributeError("EasyTracer needs a service name")

        self.service_name = config.get("service_name")
        self.logging = config.get("logging", True)
        self.sampler = config.get("sampler", dict()).get("param", 1)

    def init_tracer(self) -> Tracer:
        return Tracer(self.service_name, self.logging, self.sampler)
