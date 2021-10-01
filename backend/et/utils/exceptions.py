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
