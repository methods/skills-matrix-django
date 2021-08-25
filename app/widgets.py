from django.forms.widgets import Textarea

class GdsStyleTextarea(Textarea):
    template_name = 'app/textarea_gds_style.html'

    def __init__(self, attrs=None):
        # Use slightly better defaults than HTML's 20x2 box
        default_attrs = {'cols': '40', 'rows': '10'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)