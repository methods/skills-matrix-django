from django.core.exceptions import ValidationError


def validate_input_capitalised(value):
    if value != value.title():
        raise ValidationError('The job role title should be capitalised.')

