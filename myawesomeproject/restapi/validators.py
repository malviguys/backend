from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


def validate_name(value: str) -> None:
    if len(value) == 0:
        raise ValidationError('Lesson name must not be empty')
    if len(value) > 50:
        raise ValidationError('Lesson name must be less than 50 char')
    if not value[0].isupper():
        raise ValidationError('Lesson name must be capitalized')


def validate_date_time(value: datetime) -> None:
    TODAY = datetime.now()
    limitePrenotazioni = TODAY + timedelta(weeks=12)

    if value.timestamp() < TODAY.timestamp():
        raise ValidationError('Lesson date must be > now')
    if value.timestamp() > limitePrenotazioni.timestamp():
        raise ValidationError('Lesson date must not be < now + 3months')
    pass


def validate_duration(value: timedelta) -> None:
    if value <= timedelta(minutes=15):
        raise ValidationError('Lesson duration must not be > 15min')
    if value > timedelta(minutes=120):
        raise ValidationError('Lesson duration must not be < 2h')


def validate_cost(value: float) -> None:
    integerPart = int(value)
    decimalPart = value-int(value)
    if value <= 0:
        raise ValidationError("Lesson cost must be positive value")
    if decimalPart >= 100:
        raise ValidationError("The decimal part of lesson cost must be < 100")
    if value > 256:
        raise ValidationError("The maximum cost for lesson is 256$")


def validate_teacher(value: enumerate) -> None:
    pass


def validate_instrument(value: enumerate) -> None:
    pass


def validate_students(value: get_user_model) -> None:
    pass
