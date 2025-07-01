# app/web_scraper.py

import logging
import os
import re
import sys
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from markdownify import markdownify as md
from app.browser_utils import get_driver

# --- Safely import the save directory from config ---
try:
    from app.config_manager import SCRAPED_FILES_DIR
except ImportError:
    SCRAPED_FILES_DIR = None


def get_save_directory():
    """
    Determines the correct directory to save scraped files.

    Uses the path from config if it's set, otherwise defaults to the
    system's Downloads folder.
    """
    if SCRAPED_FILES_DIR:
        return SCRAPED_FILES_DIR
    else:
        # This works on Windows, Linux, and macOS
        return os.path.join(Path.home(), "Downloads")


def sanitize_filename(filename):
    """
    Removes characters from a filename that are not allowed by the OS.
    """
    return re.sub(r'[<>:"/\\|?*]', "_", filename)


def scrape_and_save(url):
    """
    Scrapes a given URL, converts the HTML content to Markdown, and saves it.

    Args:
        url (str): The URL to scrape.
    """
    print(f"-> Scraping content from: {url}")
    logging.info(f"Scraping URL: {url}")

    save_dir = get_save_directory()
    os.makedirs(save_dir, exist_ok=True)

    driver = None
    try:
        driver, browser = get_driver()
        print(f"-> Using {browser.capitalize()} to load the page...")
        driver.get(url)

        if "pdf" in driver.current_url:
            print("-> PDF file detected. Downloading...")
            logging.info("PDF file detected, saving...")
            pdf_path = os.path.join(save_dir, "scraped_document.pdf")
            with open(pdf_path, "wb") as f:
                f.write(driver.page_source.encode("utf-8"))
            print(f"✔ Successfully saved PDF to: {pdf_path}")
            logging.info(f"PDF saved to {pdf_path}")
            return

        print("-> Page loaded. Extracting content...")
        logging.info(f"Page Title: {driver.title}")
        body_element = driver.find_element(By.TAG_NAME, "body")
        html_content = body_element.get_attribute("outerHTML")

        markdown_content = md(html_content)
        sanitized_title = sanitize_filename(driver.title)
        filename = f"{sanitized_title}.md"
        output_path = os.path.join(save_dir, filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"✔ Successfully saved content to: {output_path}")
        logging.info(f"Content saved to {output_path} using {browser.capitalize()}.")

    except WebDriverException as e:
        error_text = str(e).lower()
        # This list now includes the Firefox-specific network error
        network_errors = [
            "net::err_internet_disconnected",
            "dns_probe_finished_no_internet",
            "about:neterror"
        ]

        if any(err in error_text for err in network_errors):
            print("❌ Network Error: Could not reach the URL. Please check your internet connection.", file=sys.stderr)
            logging.error(f"Network error while trying to access {url}.")
        else:
            print("❌ A browser error occurred. Run with --debug for details.", file=sys.stderr)
            logging.error(f"WebDriverException while scraping '{url}'. Full error: {e}")

    except Exception as e:
        # Catch any other unexpected errors
        print("❌ An unknown error occurred. Run with --debug to see technical details.", file=sys.stderr)
        logging.error(f"Failed to scrape '{url}'. Full error: {e}")
    finally:
        if driver:
            driver.quit()
