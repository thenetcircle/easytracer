from et.common.models.reprs import Event
from et.utils.exceptions import ValidationError


class Validator:
    @staticmethod
    def validate(event: Event) -> None:
        if event is None:
            raise ValidationError("event is none")
