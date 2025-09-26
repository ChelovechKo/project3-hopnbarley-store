import re
from django.core.exceptions import ValidationError


def validate_phone(value):
    if not re.match(r'^\+?[1-9]\d{7,14}$', value):
        raise ValidationError('Phone number must be between 8 and 15 digits.')
    return value
