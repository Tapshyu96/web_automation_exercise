import datetime
import os
from urllib import request

import pytest
from pytest_metadata.plugin import metadata_key
from selenium import webdriver
from pytest_metadata.plugin import metadata_key
from datetime import datetime

@pytest.fixture()
def setup(browser):
    global driver
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "ie":
        driver = webdriver.Ie()
    elif browser == "safari":
        driver = webdriver.Safari()
    elif browser == "edge":
        driver = webdriver.Edge()
    else:
        raise ValueError("Unsupported browser")

    yield driver
    driver.quit()

    return driver




def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help = "Select browser")

@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")

def pytest_configure(config):
    config.stash[metadata_key]['Project Name'] = 'Automation Exercise'
    config.stash[metadata_key]['Test Module Name'] = 'Login and Register'
    config.stash[metadata_key]['Tester Name'] = 'Tapshyu Ganvir'

    today = datetime.now().strftime("%Y-%m-%d")
    reports_dir = os.path.join("reports", today)
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    timestamp = datetime.now().strftime("%H-%M-%S")
    config.option.htmlpath = os.path.join(reports_dir, f"report_{timestamp}.html")

# @pytest.mark.optionalhook
# def pytest_metadata(metadata):
#     metadata.pop('Plugins',None)

@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata.pop('Plugins',None)

def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([f"Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    driver = item.funcargs.get("driver", None)

    if report.when == "call" and report.failed and driver:
        today = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H-%M-%S")

        screenshot_root = "screenshots"
        screenshot_dir = os.path.join(screenshot_root, today)
        os.makedirs(screenshot_dir, exist_ok=True)

        filename = f"{report.nodeid.replace('::', '_')}_{current_time}.png"
        filepath = os.path.join(screenshot_dir, filename)

        driver.save_screenshot(filepath)

        if hasattr(report, "extra"):
            from pytest_html import extras
            report.extra.append(extras.image(filepath))
