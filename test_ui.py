"""Lab 5: automate login, create a task, mark it complete, log out.

Fill in pages/task_page.py first (it has TODO markers), then write the
four test functions below.

Run with:
    pytest test_ui.py -v --html=report.html --self-contained-html

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo1234"
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.task_page import NewTaskPage, TaskListPage

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo1234"


def test_login_with_valid_credentials(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)
    # Wait for something on the next page that proves login worked
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(NewTaskPage.TITLE_INPUT)
    )
    assert "New Task" in driver.title


def test_login_with_invalid_credentials(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login("demo", "wrong-password")
    error = login_page.wait_for_error()
    assert "Invalid username or password" in error.text


def test_create_task(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)

    new_task_page = NewTaskPage(driver, base_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(new_task_page.TITLE_INPUT)
    )
    new_task_page.create_task(
        title="Prepare slides",
        priority="2",
        due_date="2026-12-01",
        hours="3"
    )
    banner = new_task_page.wait_for_success()
    assert banner.is_displayed()
    assert "Task created" in banner.text


def test_mark_task_complete_and_logout(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)

    new_task_page = NewTaskPage(driver, base_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(new_task_page.TITLE_INPUT)
    )
    new_task_page.create_task(
        title="Prepare slides",
        priority="2",
        due_date="2026-12-01",
        hours="3"
    )
    new_task_page.wait_for_success()

    task_list_page = TaskListPage(driver, base_url)
    task_list_page.open()

    # Determine task ID to complete: task 1 if complete button exists,
    # otherwise the first available pending task button on a shared server.
    complete_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[data-task-id="1"]')
    if complete_buttons:
        task_id = 1
    else:
        pending_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.complete-btn"))
        )
        task_id = int(pending_btn.get_attribute("data-task-id"))

    task_list_page.mark_complete(task_id)
    task_list_page.wait_until_completed(task_id)

    status_cell = driver.find_element(*task_list_page.status_cell(task_id))
    assert "Completed" in status_cell.text

    # Click the logout link (id="logout-link") and confirm return to login page
    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "logout-link"))
    )
    logout_link.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(LoginPage.USERNAME_INPUT)
    )
    assert "Log in" in driver.title
