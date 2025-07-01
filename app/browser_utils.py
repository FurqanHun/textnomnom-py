# app/browser_utils.py

import os
import sys
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from app.config_manager import (
    GECKO_DRIVER_PATH,
    CHROME_DRIVER_PATH,
    CHROMIUM_BASED_BROWSER_PATH,
    FIREFOX_BASED_BROWSER_PATH,
)

def get_driver():
    """
    Initializes and returns a web driver, providing specific, actionable errors.
    """
    # --- Attempt 1: Chrome ---
    chrome_path = (
        CHROMIUM_BASED_BROWSER_PATH or
        ("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" if sys.platform == "win32" else "/usr/bin/google-chrome")
    )
    if os.path.exists(chrome_path):
        # If browser is found, the driver becomes the critical missing piece.
        if not CHROME_DRIVER_PATH or not os.path.exists(CHROME_DRIVER_PATH):
            raise EnvironmentError(
                "❌ Chrome is installed, but its driver is missing or not configured.\n"
                "   Please set a valid CHROME_DRIVER_PATH in app/config_manager.py using --config"
            )
        try:
            chrome_options = ChromeOptions()
            chrome_options.binary_location = chrome_path
            chrome_options.add_argument("--headless")
            chrome_service = ChromeService(executable_path=CHROME_DRIVER_PATH)
            print("-> Initializing Chrome driver...")
            return webdriver.Chrome(service=chrome_service, options=chrome_options), "chrome"
        except Exception as e:
            # If it fails to start for another reason, we'll just let it fall through to try Firefox.
            logging.warning(f"Chrome found but failed to start: {e}")

    # --- Attempt 2: Firefox ---
    firefox_path = (
        FIREFOX_BASED_BROWSER_PATH or
        ("C:\\Program Files\\Mozilla Firefox\\firefox.exe" if sys.platform == "win32" else "/usr/bin/firefox")
    )
    if os.path.exists(firefox_path):
        # If browser is found, the driver is the critical part.
        if not GECKO_DRIVER_PATH or not os.path.exists(GECKO_DRIVER_PATH):
            raise EnvironmentError(
                "❌ Firefox is installed, but its driver is missing or not configured.\n"
                "   Please set a valid GECKO_DRIVER_PATH in app/config_manager.py using --config"
            )
        try:
            firefox_options = FirefoxOptions()
            firefox_options.binary_location = firefox_path
            firefox_options.add_argument("--headless")
            firefox_service = FirefoxService(executable_path=GECKO_DRIVER_PATH)
            print("-> Initializing Firefox driver...")
            return webdriver.Firefox(service=firefox_service, options=firefox_options), "firefox"
        except Exception as e:
            logging.warning(f"Firefox found but failed to start: {e}")

    # --- Final Fallback ---
    # If we get here, neither browser was found or could be launched.
    raise EnvironmentError(
        "Could not find a working browser installation. "
        "Please install Chrome or Firefox and configure its driver path."
    )
