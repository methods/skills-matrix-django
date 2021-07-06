from django.core.exceptions import ValidationError
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def validate_domain_email(value):
    if(re.match(regex, value)):
        if not "methods.co.uk" in value.split('@', 1)[-1]:
            raise ValidationError("Enter your Methods email address in the correct format, like firstname.surname@methods.co.uk")
    return value

def password_validation(value):
    special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
    if len(value) < 8:
        raise ValidationError('Password length must be greater than 8 character.')
    if not any(char.isdigit() for char in value):
        raise ValidationError('Password must contain at least %(min_length)d digit.'% {'min_length': 1})
    if not any(char.isalpha() for char in value):
        raise ValidationError('Password must contain at least %(min_length)d letter.' % {'min_length': 1})
    if not any(char in special_characters for char in value):
        raise ValidationError('Password must contain at least %(min_length)d special character.' % {'min_length': 1})