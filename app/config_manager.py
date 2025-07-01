# app/config_manager.py

# --- Optional ---
# Define the path for the virtual environment.
# If set to None or not defined, it defaults to a 'venv' folder in the project root.
VENV_PATH = "/mnt/qanhdd/some-stuff/pysss/textnomnom-py/venv/"

# If you have installed drivers, update paths here. Use "" or None.
GECKO_DRIVER_PATH = "/mnt/qanhdd/some-stuff/geckodriver"
CHROME_DRIVER_PATH = None

CHROMIUM_BASED_BROWSER_PATH = None
FIREFOX_BASED_BROWSER_PATH = "/usr/bin/mullvad-browser"

# --- Optional ---
# Define the directory where logs will be stored.
# If this is not set, it will default to a 'logs/' folder.
LOG_DIRECTORY = "logs"

# --- Optional ---
# Set to True to enable logging to a file without console output.
# The --debug flag will override this and log to both file and console.
LOGS = True

# --- Optional ---
# Define where scraped web content will be saved.
# If this is set to None or is not defined, it will default to your system's Downloads folder.
SCRAPED_FILES_DIR = None
