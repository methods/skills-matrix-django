from django.core.exceptions import ValidationError


def validate_input_capitalised(value):
    if value != value.title():
        raise ValidationError('The job role title should be capitalised.')


def validate_option_selected(value):
    if value == '':
        raise ValidationError('Please select one of the options.')
