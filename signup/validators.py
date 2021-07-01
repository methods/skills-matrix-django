from django.core.exceptions import ValidationError
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def validate_domain_email(value):
    if(re.match(regex, value)):
        if not "methods.co.uk" in value.split('@', 1)[-1]:
            raise ValidationError("Please enter your Methods email address in the correct format, like firstname.surname@methods.co.uk.")
    return value