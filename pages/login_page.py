"""Page Object for the login page."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.ID, "login-error")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url + "/login")
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(self.USERNAME_INPUT)
        )

    def is_loaded(self, timeout=10) -> bool:
        """Confirms the login page is loaded and ready for interaction."""
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        )
        return element.is_displayed()

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def wait_for_error(self, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        )
