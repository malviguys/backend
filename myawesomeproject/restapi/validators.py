from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, date


def validate_name(value: str) -> None:
    if len(value) > 50:
        raise ValidationError(message='Name must be less than 50 char')
    if not value[0].isupper():
        raise ValidationError(message='Name must be capitalized')


def validate_date_time(value: datetime) -> None:
    TODAY = datetime.now()
    limitePrenotazioni = TODAY + timedelta(weeks=12)

    if value.timestamp() < TODAY.timestamp():
        raise ValidationError(message='Lesson date_time cannot be in the past')
    if value.timestamp() > limitePrenotazioni.timestamp():
        raise ValidationError(
            message='Lesson date must not be < now + 3months')
    pass


def validate_duration(value: timedelta) -> None:
    if value <= timedelta(minutes=15):
        raise ValidationError(message='Lesson duration must not be > 15min')
    if value > timedelta(minutes=120):
        raise ValidationError(message='Lesson duration must not be < 2h')


def validate_cost(value: float) -> None:
    decimalPart = value-int(value)
    if value <= 0:
        raise ValidationError(message="Lesson cost must be positive value")
    if value > 256:
        raise ValidationError(message="The maximum cost for lesson is 256$")
