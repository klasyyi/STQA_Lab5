# STQA Lab 5: Web UI Automation

Automated UI test suite for the PyTodo web app using Selenium and pytest.

## What was done

- **Page Object Model (POM)**:
  - `pages/login_page.py`: Handles login interactions and error alerts.
  - `pages/task_page.py`: Implemented `NewTaskPage` (task creation, banner detection) and `TaskListPage` (status check, completion).
- **Explicit Waits**: Zero `time.sleep` used. All dynamic actions and background JS delays use `WebDriverWait` with `expected_conditions`.
- **Test Suite (`test_ui.py`)**:
  - `test_login_with_valid_credentials`
  - `test_login_with_invalid_credentials`
  - `test_create_task`
  - `test_mark_task_complete_and_logout`

## How to run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set target URL and execute tests:
```powershell
$env:PYTODO_URL="https://pytodo-lab5.onrender.com"
python -m pytest test_ui.py -v --html=report.html --self-contained-html
```

## Deliverables
- `report.html`: Self-contained HTML execution report.
- `screenshots/`: Captured browser screenshots for all test steps.
