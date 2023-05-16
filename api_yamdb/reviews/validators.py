from datetime import datetime
from django.core.exceptions import ValidationError


def validator_year(value):
    year = datetime.now().year
    if value > year:
        raise ValidationError(
            f"Год произведения не может быть больше текущего {year}"
        )
