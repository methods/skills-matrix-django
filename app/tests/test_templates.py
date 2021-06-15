from django.test import SimpleTestCase


class SimpleTests(SimpleTestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_body_resp(self):
        response = self.client.get('/')
        self.assertTrue("Welcome" in response.content)
