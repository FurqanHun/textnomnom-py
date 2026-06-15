# app/logger_config.py

import logging
import sys
import os

# Import configured log directory with fallback to working directory logs folder
try:
    from app.config_manager import LOG_DIRECTORY
    if LOG_DIRECTORY is None:
        LOG_DIRECTORY = os.path.join(os.getcwd(), "logs")
except ImportError:
    LOG_DIRECTORY = os.path.join(os.getcwd(), "logs")

# Define log filename and path
LOG_FILENAME = "textnomnom.log"
FULL_LOG_PATH = os.path.join(LOG_DIRECTORY, LOG_FILENAME)


def _ensure_log_dir_exists():
    """
    Creates the log directory if it does not exist.
    Exits the program with code 1 if directory creation fails due to OS errors.
    """
    try:
        os.makedirs(LOG_DIRECTORY, exist_ok=True)
    except OSError as e:
        print(
            f"Error: Could not create log directory at '{LOG_DIRECTORY}'. Reason: {e}",
            file=sys.stderr,
        )
        sys.exit(1)


def setup_logging(debug_mode=False):
    """
    Configures logging based on the debug flag and config settings.
    - debug_mode=True: Logs to both file and console.
    - LOGS=True in config: Logs to file only.
    """
    try:
        from app.config_manager import LOGS
    except ImportError:
        LOGS = False

    handlers = []
    if debug_mode:
        _ensure_log_dir_exists()
        handlers.append(logging.FileHandler(FULL_LOG_PATH, encoding="utf-8"))
        handlers.append(logging.StreamHandler(sys.stdout))
    elif LOGS:
        _ensure_log_dir_exists()
        handlers.append(logging.FileHandler(FULL_LOG_PATH, encoding="utf-8"))

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
        if os.path.exists(FULL_LOG_PATH):
            with open(FULL_LOG_PATH, "w", encoding="utf-8") as file:
                file.truncate(0)
            logging.info(f"Log file '{FULL_LOG_PATH}' has been cleared.")
        else:
            logging.info(f"Log file '{FULL_LOG_PATH}' does not exist; nothing to clear.")
    except Exception as e:
        logging.error(f"An error occurred while clearing the log file: {e}")
