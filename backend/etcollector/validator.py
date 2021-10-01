from backend.utils.exceptions import ValidationError


class Validator:
    @staticmethod
    def validate(event: dict) -> None:
        if event is None:
            raise ValidationError("event is none")
