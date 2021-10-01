from et.collector.models.event import Event


class ValidationError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"ValidationError: {self.msg}"


class ParseError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"ParseError: {self.msg}"


class CollectorException(Exception):
    def __init__(self, status_code: int, parent: Exception, event: Event):
        self.status_code = status_code
        self.parent = parent
        self.event = event
