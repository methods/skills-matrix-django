from django.forms import Select


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
        # if not value:
        #     option_dict['attrs']['disabled'] = True
        if value in self.disabled_choices:
            option_dict['attrs']['disabled'] = True
        return option_dict
