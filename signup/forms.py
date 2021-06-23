from django import forms


class NameForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'govuk-input'}))
    surname = forms.CharField(label='Surname', max_length=100,
                              widget=forms.TextInput(attrs={'class': 'govuk-input'}))
