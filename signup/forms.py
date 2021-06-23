from django import forms


class NameForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'govuk-input'}))
    surname = forms.CharField(label='Surname', max_length=100,
                              widget=forms.TextInput(attrs={'class': 'govuk-input'}))


class EmailForm(forms.Form):
    email_address = forms.EmailField(label='Email address', max_length=100,
                                     widget=forms.TextInput(attrs={'class': 'govuk-input'}))
