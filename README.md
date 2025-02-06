# TextNomNom

This Python script extracts text from PDFs and PowerPoint files (including images with OCR), converts PowerPoints to PDFs, and scrapes web pages into Markdown. Supports both single files and directories (recursive processing).

## Features:

- **Text Extraction:** Pulls text from PDFs and PowerPoints (OCR for images too!).
- **PowerPoint Conversion:** Converts your PowerPoint files (.ppt/.pptx) to PDF.
- **Directory Processing:** Processes all supported files within a specified directory (recursively).
- **Flexible Output:** Saves extracted text to either a single file or individual files for each document.
- **Web Scraping:** Grabs website content and converts it to clean Markdown.

## Requirements:

- **Python 3.x**
- **Libraries:**
  - `PyPDF2` for PDF text extraction.
  - `python-pptx` for PowerPoint text extraction.
  - `win32com.client` (for Windows users) for PowerPoint to PDF conversion and `.ppt` to `.pptx` conversion (required by the `python-pptx` library).
  - `unoconv` or `soffice` (for Linux users) for PowerPoint to PDF conversion and `.ppt` to `.pptx` conversion (required by the `python-pptx` library).
  - **URL Scrapping:**
    - `selenium` for web scraping.
    - `beautifulsoup4` for parsing HTML content.
    - `markdownify` for converting HTML to markdown.
    - Webdriver for browser automation
      - [ChromeDriver](https://developer.chrome.com/docs/chromedriver/)
      - [GeckoDriver](https://github.com/mozilla/geckodriver/tree/release)

- **OCR (Beta Feature):**
  - `pytesseract`, `Pillow`, and `pdf2image` for OCR-based text extraction.

  - **`tesseract-ocr`**: Required by `pytesseract` for OCR functionality.
    - [tesseract-ocr GitHub](https://github.com/tesseract-ocr/tesseract)
    - Available in the package manager of most Linux distributions and can be installed on Windows and macOS.

  - **`poppler-utils`**: For PDF to text conversion.
    - [poppler-utils](https://poppler.freedesktop.org/) or you can use prebuilt binaries from third-party sources like [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases)
    - Available in the package manager of most Linux distributions and can be installed on Windows and macOS.

## Platform-Specific Notes:

- On **Linux** systems: Uses **LibreOffice** for PowerPoint file conversions (via `soffice` or `unoconv`).
- On **Windows** systems: Uses **Microsoft Office (PowerPoint)** for PowerPoint file conversions (via `win32com.client`).

tldr; uses LibreOffice on linux systems and ms office (PowerPoint) on windows systems.

## Installation:

1. Install the required Python libraries:
   ```bash
   pip install PyPDF2 python-pptx pytesseract pillow pdf2image selenium markdownify
   ```
   _beautifusoup4 is a dependency of markdownify, so you don't need to install it separately._

2. For PowerPoint to PDF conversion:
   - **Windows:** Ensure Microsoft PowerPoint is installed. The script uses `win32com.client` to automate PowerPoint.
   ```bash
    pip install pywin32
    ```
   - **Linux:** Install `unoconv` or `soffice` (part of LibreOffice).
      - soffice comes inbuilt with LibreOffice, which pretty much available in all linux distros, and comes as a default in some.
      - if you wanna use unoconv, you can install that too (which also requires LibreOffice).

3. For OCR-based text extraction:
    - Install `tesseract-ocr` and `poppler-utils`:
      - **Linux:** Use the package manager of your distribution.
        ```bash
        sudo apt-get install tesseract-ocr poppler-utils
        ```
          - Fedora:
              ```bash
              sudo dnf install tesseract poppler-utils
              ```
      - **Windows:** Download and install `tesseract-ocr` from the [official repository](https://github.com/tesseract-ocr/tesseract)
      - **Windows:** Download and install `poppler-utils` from the [official repository](https://poppler.freedesktop.org/)

## Usage:

```bash
python main.py <file_or_directory_path> [options]
```

## Options:

- `-h, --help`: Show help message and exit.
- `-a`: Save all extracted text from files in the directory to a single text file (`all_extracted_text.txt`).
- `--convert pdf`: Convert PowerPoint (.ppt or .pptx) to PDF.
- `-ocr, --ocr`: Trigger OCR extraction for image files.

### Examples:

1. **Process a Single File:**
   ```bash
   python main.py document.pdf
   ```
   This command extracts text from `document.pdf` and saves it as `document.txt` in the same directory.

2. **Process a Directory:**
   ```bash
   python main.py /path/to/directory
   ```
   This command processes all supported files in the specified directory, saving the extracted text to individual `.txt` files within an `extracted_texts` subdirectory.

3. **Save All Extracted Text to a Single File:**
   ```bash
   python main.py /path/to/directory -a
   ```
   This command processes all supported files in the specified directory and saves all extracted text to `all_extracted_text.txt` within the `extracted_texts` subdirectory.

4. **Convert PowerPoint to PDF:**
   ```bash
   python main.py presentation.pptx --convert pdf
   ```
   This command converts `presentation.pptx` to `presentation.pdf` in the same directory.

5. **OCR Extraction from an Image:**
   ```bash
   python main.py image.jpg -ocr
   ```
   This command extracts text from `image.jpg` using OCR and saves the output as `image.txt` in the same directory.

6. **OCR Extraction from All Image Files in a Directory:**
   ```bash
   python main.py /path/to/directory -ocr
   ```
   This command processes all image files in the specified directory using OCR, saving extracted text to individual `.txt` files within an `extracted_texts` subdirectory.

7. **OCR Extraction from Images in a PowerPoint Presentation:**
   ```bash
   python main.py presentation.pptx -ocr
   ```
   This command extracts text from any images in the PowerPoint presentation `presentation.pptx` using OCR and saves it as `presentation.txt` in the same directory.

8. **URL Scrapping:**
   ```bash
   python main.py https://example.com
   ```

## Logging:

The script logs its operations to `file_processing.log` and also outputs logs to the console.

### Notes:

- Ensure that the necessary conversion tools (`win32com.client`, `unoconv`, or `soffice`) are installed and accessible in your system's PATH.
- The script skips `.txt` files within the `extracted_texts` subdirectory to avoid processing already extracted text.
- Tessaract OCR is a beta feature, and it may not work as expected. It is recommended to use it only for image files.
- Tessaract and poppler-utils are must for OCR and PDF to text conversion respectively.
- The `selenium` library requires a WebDriver for browser automation. Download the appropriate WebDriver for your browser and add its path in the script if you plan to use the URL scraping feature.

## License:

This project is licensed under the [GPL-3.0 License](LICENSE). Feel free to use, modify, and distribute the code as per the terms of the license.
