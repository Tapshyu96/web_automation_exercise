import os
import pytest
from datetime import datetime
from selenium import webdriver
from pytest_metadata.plugin import metadata_key


# =========================
# CLI OPTION
# =========================
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Select browser: chrome | firefox | edge"
    )


# =========================
# SETUP FIXTURE
# =========================
@pytest.fixture()
def setup(browser):
    # browser = request.config.getoption("--browser")
    global driver
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "edge":
        driver = webdriver.Edge()
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")
# =========================
# PYTEST METADATA
# =========================
def pytest_configure(config):
    config.stash[metadata_key]["Project Name"] = "Automation Exercise"
    config.stash[metadata_key]["Test Module Name"] = "Login and Register"
    config.stash[metadata_key]["Tester Name"] = "Tapshyu Ganvir"

    today = datetime.now().strftime("%Y-%m-%d")
    reports_dir = os.path.join("reports", today)
    os.makedirs(reports_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%H-%M-%S")
    config.option.htmlpath = os.path.join(
        reports_dir, f"report_{timestamp}.html"
    )


@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata.pop("Plugins", None)


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([
        f"Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ])


# =========================
# SCREENSHOT ON FAILURE
# =========================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    driver = item.funcargs.get("setup")

    if report.when == "call" and report.failed and driver:
        today = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H-%M-%S")

        screenshot_dir = os.path.join("screenshots", today)
        os.makedirs(screenshot_dir, exist_ok=True)

        filename = f"{item.name}_{current_time}.png"
        filepath = os.path.join(screenshot_dir, filename)

        driver.save_screenshot(filepath)

        if hasattr(report, "extra"):
            from pytest_html import extras
            report.extra.append(extras.image(filepath))
