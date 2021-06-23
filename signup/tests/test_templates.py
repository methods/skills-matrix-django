from django.test import LiveServerTestCase
from selenium import webdriver
from django.urls import reverse


class AddNameSignup(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.headless = True
        cls.browser = webdriver.Firefox(options=fireFoxOptions)
        cls.browser.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.headless = True
        cls.browser = webdriver.Firefox(options=fireFoxOptions)
        cls.browser.quit()
        super().tearDownClass()

    def complete_url(self, url):
        return self.live_server_url + url

    def test_signup_add_name_page_status_code(self):
        response = self.client.get('/signup/name')
        assert response.status_code == 200

    def test_signup_add_name_body_resp(self):
        response = self.client.get('/signup/name')
        assert "What is your name?" in response.content.decode()

    def test_submit_redirects_to_email_page(self):
        self.browser.get(self.complete_url('/signup/name'))
        self.browser.find_element_by_id('id_first_name').send_keys("user_first_name")
        self.browser.find_element_by_id('id_surname').send_keys("user_surname")
        self.browser.find_element_by_class_name("govuk-button").click()
        assert self.complete_url('/signup/email/') == self.browser.current_url
