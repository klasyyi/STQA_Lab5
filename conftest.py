"""Shared pytest configuration, fixtures, and HTML reporting hooks.

Captures browser screenshots upon test completion and embeds them
into the self-contained pytest-html report.
"""
import base64
import logging
import os
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)

BASE_URL = os.environ.get("PYTODO_URL", "http://127.0.0.1:5000")
RESET_TOKEN = os.environ.get("PYTODO_RESET_TOKEN", "lab5reset")


def _sanitize_metadata(metadata):
    """Removes host-specific paths and injects clean project details."""
    for noisy_key in ["JAVA_HOME", "CI", "COMMAND_LINE"]:
        metadata.pop(noisy_key, None)
    metadata["Test Suite"] = "STQA Lab 5 Web UI Automation"
    metadata["Target Application"] = BASE_URL
    metadata["Execution Mode"] = "Google Chrome (Headless)"


def pytest_configure(config):
    """Sanitizes environment metadata and adds structured project details."""
    if hasattr(config, "_metadata"):
        _sanitize_metadata(config._metadata)
    try:
        from pytest_metadata.plugin import metadata_key
        if metadata_key in config.stash:
            _sanitize_metadata(config.stash[metadata_key])
    except ImportError:
        pass


@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata, config):
    """pytest-metadata hook called to finalize session metadata."""
    _sanitize_metadata(metadata)


@pytest.fixture(scope="session", autouse=True)
def reset_app_state_before_run():
    """Attempts to clear tasks on the server before the test suite begins.
    Logs an informative note if the endpoint is protected (e.g. HTTP 403 on shared deployments)
    or unreachable, allowing tests to proceed with dynamic pending task resolution.
    """
    try:
        resp = requests.post(
            f"{BASE_URL}/admin/reset",
            params={"token": RESET_TOKEN},
            timeout=10
        )
        if resp.status_code == 200:
            logger.info("Application state successfully reset.")
        else:
            logger.info(
                f"Reset endpoint returned HTTP {resp.status_code}. "
                "Tests will resolve active task IDs dynamically."
            )
    except requests.RequestException as exc:
        logger.info(
            f"Reset endpoint unreachable ({exc}). "
            "Proceeding with dynamic task state."
        )


@pytest.fixture
def driver():
    """Creates a headless Google Chrome WebDriver session."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()


@pytest.fixture
def base_url():
    """Provides the target application URL."""
    return BASE_URL


def pytest_html_report_title(report):
    """Sets a professional title for the HTML test execution report."""
    report.title = "STQA Lab 5: Web UI Automation Report"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captures a screenshot at the end of each test call and attaches it to the report."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    driver = item.funcargs.get("driver")
    if driver is None:
        return

    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    file_name = f"{screenshots_dir}/{item.name}.png"
    driver.save_screenshot(file_name)

    extra = getattr(report, "extras", [])
    try:
        from pytest_html import extras
        with open(file_name, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode("utf-8")
        extra.append(extras.image(b64_data, name="Screenshot"))
        report.extras = extra
    except Exception as exc:
        logger.warning(f"Failed to attach screenshot for {item.name}: {exc}")
