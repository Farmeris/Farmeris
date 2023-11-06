from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

def custom_password_validation(password):
    try:
        validate_password(password)
    except ValidationError as error:
        raise ValidationError("Zle heslo.")
