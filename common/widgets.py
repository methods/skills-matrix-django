from django.forms.widgets import Input
from django.forms import Select


class GdsStylePasswordInput(Input):
    template_name = "user_management/gds_input.html"
    input_type = 'password'

    def __init__(self, attrs=None, render_value=False):
        super().__init__(attrs)
        self.render_value = render_value

    def get_context(self, name, value, attrs):
        if not self.render_value:
            value = None
        return super().get_context(name, value, attrs)


class GdsStyleTextInput(Input):
    template_name = "user_management/gds_input.html"
    input_type = 'text'


class GdsStyleEmailInput(Input):
    input_type = 'email'
    template_name = 'user_management/gds_input.html'


class CustomisedSelectWidget(Select):
    def __init__(self, *args, disabled_choices=[], **kwargs):
        self._disabled_choices = disabled_choices
        super(CustomisedSelectWidget, self).__init__(*args, **kwargs)

    @property
    def disabled_choices(self):
        return self._disabled_choices

    @disabled_choices.setter
    def disabled_choices(self, other):
        self._disabled_choices = other

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option_dict = super(CustomisedSelectWidget, self).create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        if value in self.disabled_choices:
            option_dict['attrs']['disabled'] = True
        return option_dict
