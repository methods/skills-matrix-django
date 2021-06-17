from django.test import LiveServerTestCase
from selenium import webdriver



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

    def test_add_name_form_submission(self):
        self.browser.get(self.complete_url('/signup/name'))
        self.browser.find_element_by_id('firstName').send_keys("user_first_name")
        self.browser.find_element_by_id('surname').send_keys("user_surname")
        self.browser.find_element_by_class_name("govuk-button").click()
        session = self.client.session
        assert "user_first_name" in session.temp_profile
        assert "user_surname" in session.temp_profile
