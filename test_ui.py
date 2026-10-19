"""STQA Lab 5: Automated UI Acceptance Suite for PyTodo application."""
from pages.login_page import LoginPage
from pages.task_page import NewTaskPage, TaskListPage

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo1234"


def test_login_with_valid_credentials(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)

    new_task_page = NewTaskPage(driver, base_url)
    assert new_task_page.is_loaded()
    assert "New Task" in driver.title


def test_login_with_invalid_credentials(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(DEMO_USERNAME, "wrong-password")

    error_banner = login_page.wait_for_error()
    assert "Invalid username or password" in error_banner.text


def test_create_task(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)

    new_task_page = NewTaskPage(driver, base_url)
    assert new_task_page.is_loaded()
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
    assert new_task_page.is_loaded()
    new_task_page.create_task(
        title="Prepare slides",
        priority="2",
        due_date="2026-12-01",
        hours="3"
    )
    new_task_page.wait_for_success()

    task_list_page = TaskListPage(driver, base_url)
    task_list_page.open()

    task_id = task_list_page.get_first_pending_task_id()
    task_list_page.mark_complete(task_id)
    task_list_page.wait_until_completed(task_id)
    assert "Completed" in task_list_page.get_status(task_id)

    task_list_page.logout()
    assert login_page.is_loaded()
    assert "Log in" in driver.title
