# app/config_manager.py
import os

# ==============================================================================
# TextNomNom Configuration Management
# ==============================================================================

# VENV_PATH (str):
# The directory path to the Python virtual environment. Used by the subprocess 
# runner to locate the correct environment binaries. 
# Default: "venv" (resolves to the 'venv' folder in the project root directory).
VENV_PATH = "venv"

# GECKO_DRIVER_PATH (str / None):
# The file path to the Geckodriver executable used for Firefox-based scraping.
# Set to None if Geckodriver is not needed or is installed in the system PATH.
GECKO_DRIVER_PATH = None

# CHROME_DRIVER_PATH (str / None):
# The file path to the Chromedriver executable used for Chrome/Chromium scraping.
# Set to None if Chromedriver is not needed or is installed in the system PATH.
CHROME_DRIVER_PATH = None

# CHROMIUM_BASED_BROWSER_PATH (str / None):
# The binary path of a Chromium-based web browser (e.g. Chrome, Brave, Chromium).
# If None, the application falls back to standard system paths.
CHROMIUM_BASED_BROWSER_PATH = None

# FIREFOX_BASED_BROWSER_PATH (str / None):
# The binary path of a Firefox-based web browser (e.g. Firefox, Mullvad Browser).
# If None, the application falls back to standard system paths.
FIREFOX_BASED_BROWSER_PATH = None

# LOG_DIRECTORY (str):
# The directory name or path where logging output files will be written.
# Default: "logs"
LOG_DIRECTORY = "logs"

# LOGS (bool):
# Toggle for file-based logging. If set to True, logs are written to the file
# specified in LOG_DIRECTORY without stdout console output, unless --debug is set.
# Default: False
LOGS = False

# SCRAPED_FILES_DIR (str / None):
# Directory where scraped markdown and document contents will be saved.
# If set to None, defaults to the user's system Downloads directory.
SCRAPED_FILES_DIR = None

# MAX_OCR_WORKERS (int):
# The maximum number of worker threads to use in ThreadPoolExecutor for OCR tasks.
# Defaults to one less than the total CPU cores to keep the system responsive.
MAX_OCR_WORKERS = max(1, (os.cpu_count() or 4) - 1)
