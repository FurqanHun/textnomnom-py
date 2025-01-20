**Text Extraction and Conversion Tool**

This Python script facilitates the extraction of text from PDF and PowerPoint files, with options to convert PowerPoint presentations to PDF. It supports both individual files and directories, saving extracted text either to a single file or separate files for each processed document.

**Features:**

- **Text Extraction:** Extracts text from PDF and PowerPoint (.pptx) files.
- **PowerPoint Conversion:** Converts PowerPoint presentations (.ppt or .pptx) to PDF format.
- **Directory Processing:** Processes all supported files within a specified directory.
- **Flexible Output:** Saves extracted text to a single file or individual files for each document.

**Requirements:**

- Python 3.x
- `PyPDF2` library for PDF text extraction
- `python-pptx` library for PowerPoint text extraction
- `win32com.client` (for Windows users) for PowerPoint to PDF conversion and ppt to pptx conversion (which is required for the `python-pptx` library)
- `unoconv` or `soffice` (for Linux users) for PowerPoint to PDF conversion and ppt to pptx conversion (which is required for the `python-pptx` library)

tldr; uses LibreOffice on linux systems and ms office (PowerPoint) on windows systems.

**Installation:**

1. Install the required Python libraries:

   ```bash
   pip install PyPDF2 python-pptx
   ```

2. For PowerPoint to PDF conversion:
   - **Windows:** Ensure Microsoft PowerPoint is installed. The script uses `win32com.client` to automate PowerPoint.
   ```bash
    pip install pywin32
    ```
   - **Linux:** Install `unoconv` or `soffice` (part of LibreOffice).
      - soffice comes inbuilt with LibreOffice, which pretty much available in all linux distros, and comes as a default in some.
      - if you wanna use unoconv, you can install that too (which also requires LibreOffice).

**Usage:**

```bash
python main.py <file_or_directory_path> [options]
```

**Options:**

- `-h, --help`: Show help message and exit.
- `-a`: Save all extracted text from files in the directory to a single text file (`all_extracted_text.txt`).
- `--convert pdf`: Convert PowerPoint (.ppt or .pptx) to PDF.

**Examples:**

1. **Process a Single File:**

   ```bash
   python main.py document.pdf
   ```

   This command extracts text from `document.pdf` and saves it as `document.txt` in the same directory.

2. **Process a Directory:**

   ```bash
   python main.py /path/to/directory
   ```

   This command processes all supported files in the specified directory, saving extracted text to individual `.txt` files within an `extracted_texts` subdirectory.

3. **Save All Extracted Text to a Single File:**

   ```bash
   python main.py /path/to/directory -a
   ```

   This command processes all supported files in the specified directory and saves all extracted text to `all_extracted_text.txt` in the `extracted_texts` subdirectory.

4. **Convert PowerPoint to PDF:**

   ```bash
   python main.py presentation.pptx --convert pdf
   ```

   This command converts `presentation.pptx` to `presentation.pdf` in the same directory.

**Logging:**

The script logs its operations to `file_processing.log` and also outputs logs to the console.

**Notes:**

- Ensure that the necessary conversion tools (`win32com.client`, `unoconv`, or `soffice`) are installed and accessible in your system's PATH.
- The script skips `.txt` files within the `extracted_texts` subdirectory to avoid processing already extracted text.

**License:**

This project is licensed under the [GPL-3.0 License](LICENSE). Feel free to use, modify, and distribute the code as per the terms of the license.
