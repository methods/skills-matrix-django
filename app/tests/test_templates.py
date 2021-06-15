from django.test import LiveServerTestCase
# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# options = Options()
# options.headless = True
# driver = webdriver.Firefox(options=options


class GeneralFunctionalTests(LiveServerTestCase):

    def setUp(self):
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.headless = True
        self.browser = webdriver.Firefox(options=fireFoxOptions)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

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


