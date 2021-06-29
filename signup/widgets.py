from django.forms.widgets import Input

class GdsStyleInput(Input):
    template_name="signup/gds_input.html"
    input_type = 'password'
    def __init__(self, attrs=None, render_value=False):
        super().__init__(attrs)
        self.render_value = render_value

    def get_context(self, name, value, attrs):
        if not self.render_value:
            value = None
        context = super().get_context(name, value, attrs)
        print(context)
        return context