from django.core.exceptions import ValidationError

def validate_domain_email(value):
    if '@' in value:
        if not "methods.co.uk" in value.split('@', 1)[-1]:
            raise ValidationError("Please enter your Methods email address in the correct format, like firstname.surname@methods.co.uk.")
    return value