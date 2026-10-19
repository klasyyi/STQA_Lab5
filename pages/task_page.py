"""Page Objects for the task creation page and the task list page."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NewTaskPage:
    TITLE_INPUT = (By.ID, "title")
    PRIORITY_INPUT = (By.ID, "priority")
    DUE_DATE_INPUT = (By.ID, "due_date")
    HOURS_INPUT = (By.ID, "hours")
    CREATE_BUTTON = (By.ID, "create-button")
    SUCCESS_BANNER = (By.ID, "success-banner")
    LOGOUT_LINK = (By.ID, "logout-link")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url + "/")
        self.is_loaded()

    def is_loaded(self, timeout=10) -> bool:
        """Confirms that the New Task form is visible and interactive."""
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.TITLE_INPUT)
        )
        return element.is_displayed()

    def create_task(self, title, priority, due_date, hours):
        title_el = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.TITLE_INPUT)
        )
        title_el.clear()
        title_el.send_keys(title)

        priority_el = self.driver.find_element(*self.PRIORITY_INPUT)
        priority_el.clear()
        priority_el.send_keys(priority)

        due_date_el = self.driver.find_element(*self.DUE_DATE_INPUT)
        due_date_el.clear()
        due_date_el.send_keys(due_date)

        hours_el = self.driver.find_element(*self.HOURS_INPUT)
        hours_el.clear()
        hours_el.send_keys(hours)

        self.driver.find_element(*self.CREATE_BUTTON).click()

    def wait_for_success(self, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.SUCCESS_BANNER)
        )

    def logout(self, timeout=10):
        logout_el = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.LOGOUT_LINK)
        )
        logout_el.click()


class TaskListPage:
    TASK_TABLE = (By.ID, "task-table")
    LOGOUT_LINK = (By.ID, "logout-link")
    PENDING_BUTTONS = (By.CSS_SELECTOR, "button.complete-btn")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    @staticmethod
    def complete_button(task_id):
        return (By.CSS_SELECTOR, f'button[data-task-id="{task_id}"]')

    @staticmethod
    def status_cell(task_id):
        return (By.ID, f"status-{task_id}")

    def open(self):
        self.driver.get(self.base_url + "/tasks")
        self.is_loaded()

    def is_loaded(self, timeout=10) -> bool:
        """Confirms the task table has rendered on the page."""
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.TASK_TABLE)
        )
        return element.is_displayed()

    def get_first_pending_task_id(self, preferred_id=1, timeout=10) -> int:
        """Locates an active pending task ID. Prefers `preferred_id` if available,
        otherwise resolves the first clickable pending completion button.
        """
        pref_buttons = self.driver.find_elements(*self.complete_button(preferred_id))
        if pref_buttons:
            return preferred_id

        pending_btn = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.PENDING_BUTTONS)
        )
        return int(pending_btn.get_attribute("data-task-id"))

    def mark_complete(self, task_id, timeout=10):
        button = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.complete_button(task_id))
        )
        button.click()

    def wait_until_completed(self, task_id, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(self.status_cell(task_id), "Completed")
        )

    def get_status(self, task_id, timeout=10) -> str:
        """Returns the text status for the specified task ID."""
        cell = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.status_cell(task_id))
        )
        return cell.text

    def logout(self, timeout=10):
        logout_el = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.LOGOUT_LINK)
        )
        logout_el.click()
