from django.contrib.auth.forms import AuthenticationForm
from django import forms
from signup.widgets import GdsStyleEmailInput, GdsStylePasswordInput


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=GdsStyleEmailInput(), label='Email address')
    password = forms.CharField(widget=GdsStylePasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs, use_required_attribute=False)
        attrs = {}
        attrs.update({"errors": True})
        attrs['class'] = 'govuk-input--error'
        for field in self.fields:
            if field in self.errors:
                self.fields[field].widget = GdsStyleEmailInput(attrs=attrs)