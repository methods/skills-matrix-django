from django.test import SimpleTestCase
from ..forms import NameForm

class TestForms(SimpleTestCase):
    def test_name_form_valid_data(self):
        form = NameForm(data={
            'first_name': 'user',
            'surname': 'user_surname'
        })

        assert form.is_valid()

    def test_name_form_invalid_data(self):
        form = NameForm(data={})

        assert not form.is_valid()