from django.forms.widgets import Input


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
