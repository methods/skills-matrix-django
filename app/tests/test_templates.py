from django.test import LiveServerTestCase
from selenium import webdriver


class GeneralFunctionalTests(LiveServerTestCase):

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

    def test_home_page_status_code(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_home_page_body_resp(self):
        response = self.client.get('/')
        assert "Welcome" in response.content.decode()

    def test_edit_skills_button(self):
        self.browser.get(self.complete_url('/'))
        button = self.browser.find_element_by_class_name('govuk-button')
        button.click()
        assert self.complete_url('/edit-skills') == self.browser.current_url


