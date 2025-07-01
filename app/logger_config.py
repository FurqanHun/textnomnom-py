# app/logger_config.py

import logging
import sys
import os

# --- Safely import the log directory from config ---
try:
    from app.config_manager import LOG_DIRECTORY
    if LOG_DIRECTORY is None:
        LOG_DIRECTORY = os.path.join(os.getcwd(), "logs")
except ImportError:
    LOG_DIRECTORY = os.path.join(os.getcwd(), "logs")

# --- Standardize the filename and create the full path ---
LOG_FILENAME = "textnomnom.log"
FULL_LOG_PATH = os.path.join(LOG_DIRECTORY, LOG_FILENAME)


def _ensure_log_dir_exists():
    """
    Internal helper function to create the log directory if it doesn't exist.
    This prevents errors when the logger tries to create the file.
    """
    try:
        # The 'exist_ok=True' flag prevents an error if the directory already exists.
        os.makedirs(LOG_DIRECTORY, exist_ok=True)
    except OSError as e:
        # This will catch errors like permission denied
        print(
            f"Error: Could not create log directory at '{LOG_DIRECTORY}'. Reason: {e}",
            file=sys.stderr,
        )
        # Exit gracefully if we can't create the log directory
        sys.exit(1)


def setup_logging(debug_mode=False):
    """
    Configures logging based on the debug flag and config settings.
    - debug_mode=True: Logs to both file and console.
    - LOGS=True in config: Logs to file only.
    """
    # Import here to get the latest value from the user-edited file
    try:
        from app.config_manager import LOGS
    except ImportError:
        LOGS = False

    handlers = []
    # In debug mode, always log to both file and console
    if debug_mode:
        _ensure_log_dir_exists()
        handlers.append(logging.FileHandler(FULL_LOG_PATH, encoding="utf-8"))
        handlers.append(logging.StreamHandler(sys.stdout))
    # If not in debug mode, but file logging is enabled, log to file only
    elif LOGS:
        _ensure_log_dir_exists()
        handlers.append(logging.FileHandler(FULL_LOG_PATH, encoding="utf-8"))

    # Only configure logging if there are handlers to add
    if handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=handlers,
        )
        if debug_mode:
            logging.info("Debug logging enabled (file and console).")
        elif LOGS:
            logging.info("File-only logging enabled.")


def clear_log_file():
    """Clears the content of the log file."""
    _ensure_log_dir_exists()
    try:
        # Check if the file exists before trying to open it
        if os.path.exists(FULL_LOG_PATH):
            with open(FULL_LOG_PATH, "w", encoding="utf-8") as file:
                file.truncate(0)
            logging.info(f"Log file '{FULL_LOG_PATH}' has been cleared.")
        else:
            logging.info(f"Log file '{FULL_LOG_PATH}' does not exist; nothing to clear.")
    except Exception as e:
        logging.error(f"An error occurred while clearing the log file: {e}")
