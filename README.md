# TextNomNom v2.0

[![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)](https://github.com/FurqanHun/textnomnom-py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**TextNomNom** is a versatile, cross-platform tool for extracting text from various file formats. It features a powerful command-line interface and a user-friendly interactive menu, with a self-contained environment that handles all Python dependencies automatically.

---

## Table of Contents
* [Features](#features)
* [Installation & Setup](#installation--setup)
* [External Dependencies](#external-dependencies-manual-install)
* [Usage](#usage)
  * [Interactive Mode](#interactive-mode)
  * [Command-Line Mode](#command-line-cli-mode)
* [Configuration](#configuration)
* [CLI Options](#cli-options)
* [License](#license)
---

### Features

* **Self-Contained Environment:** No more manual `pip install`. The launcher script automatically creates a virtual environment and installs all required Python packages on the first run.
* **Dual Mode Operation:**
    * **Interactive Menu:** Run without arguments to launch a user-friendly, step-by-step menu.
    * **Powerful CLI:** Use command-line arguments for scripting and automation.
* **Multi-Format Support:** Extracts text from PDFs, modern PowerPoint (`.pptx`), legacy PowerPoint (`.ppt`), and common image formats (JPG, PNG, etc.).
* **Real-Time Progress Bar:** A dynamic progress bar shows the status when processing directories, updating for every page/slide processed.
* **Web Scraping:** Provide a URL to scrape its text content into a clean Markdown file.
* **Conversion:** Converts PPT and PPTX into PDF. Bulk conversion (full directory) is also supported.
* **Advanced OCR:** Can perform OCR on images within PDFs and PowerPoint slides to capture text from all sources.
* **Cross-Platform & Configurable:** Works on Linux, macOS, and Windows. A central config file allows for easy customization of driver paths and other settings.

---

### Installation & Setup

Getting started is designed to be as simple as possible.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/FurqanHun/textnomnom-py.git
    cd textnomnom-py
    ```

2.  **(For Linux/macOS)** Make the launcher executable:
    ```bash
    chmod +x textnomnom
    ```

3.  **Run it!**
    ```bash
    ./textnomnom
    ```
    The first time you run the script, it will automatically create its virtual environment and install all necessary Python libraries. Subsequent runs will be instant. You can run it with `--config` to modify the PATHS. `--config` or `--version` both run in stage 1, before the launcher checks/sets up the virtual environment.

---

### External Dependencies (Manual Install)

For certain features, you still need to install system-level tools. The script may run without them, but the features might be limited.

* **For OCR (`--ocr`, `--ocr-mix`):** You need **Tesseract**.
    * **Fedora/CentOS:** `sudo dnf install tesseract`
    * **Debian/Ubuntu:** `sudo apt-get install tesseract-ocr`
    * **Windows/macOS:** Install from the [official Tesseract repository](https://github.com/tesseract-ocr/tesseract).

* **For PDF-to-Image Conversion (used by OCR):** You need **Poppler**.
    * **Fedora/CentOS:** `sudo dnf install poppler-utils`
    * **Debian/Ubuntu:** `sudo apt-get install poppler-utils`
    * **Windows:** Download and install from [this Poppler for Windows repo](https://github.com/oschwartz10612/poppler-windows/releases).

* **For `.ppt` to `.pptx` Conversion (Linux only):** You need **LibreOffice**.
    * This is included by default on many Linux distributions. If not, install it with your package manager (e.g., `sudo dnf install libreoffice`).

---

### Usage

You can run the application in two modes.

#### Interactive Mode
Simply run the command without any arguments to launch a guided menu.

```bash
./textnomnom
```

#### Command-Line (CLI) Mode
Provide a path or other arguments to run directly from the command line.

```bash
# Process a directory and save all text to one file with OCR
./textnomnom /path/to/my_docs -a --ocr-mix

# Scrape a website
./textnomnom https://example.com

# Get the version number instantly
./textnomnom --version
```

---
### Configuration
To open the configuration file in your default editor, run:
``` bash
./textnomnom --config
```
OR
``` bash
./textnomnom --config=EDITOR
```
Where `EDITOR` is the name of your preferred editor.

Following is the Default Configuration File:
``` py
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
```
---

### CLI Options

| Argument                  | Description                                                                 |
| ------------------------- | --------------------------------------------------------------------------- |
| `path`                    | Path to a file, directory, or a URL to process.                             |
| `-a`, `--save-all`        | Combine all extracted text from a directory into a single file.             |
| `--ocr`                   | Force OCR on image files.                                                   |
| `--ocr-mix`               | Extract both standard text and OCR text from PDFs and PPTX files.           |
| `--convert PDF`           | Converts the PPT and PPTX into PDF (Supports directories)                   |
| `--clear-log`             | Clears the content of the log file.                                         |
| `--config[=editor]`       | Opens the config file in the default editor (or a specified one).           |
| `-v`, `--version`         | Shows the application's version number.                                     |
| `--debug`                 | Enables detailed logging to the console and `logs/textnomnom.log`.          |
| `--verbose`               | Shows detailed setup steps when the launcher runs.                          |
| `-h`, `--help`            | Shows the help message for command-line options.                            |

---

### License

This project is now licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
