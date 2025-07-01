# app/file_handlers/pdf_handler.py

import logging
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
import shutil


def extract_text_from_pdf(file_path, trigger_ocr=False, ocr_mix=False, callback=None):
    """Extracts text from a PDF, with an option for OCR."""
    text_content = []
    try:
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if text:
                    text_content.append(text)

                if trigger_ocr or ocr_mix:
                    # Proactive checks for Tesseract and Poppler
                    if not shutil.which("tesseract"):
                        raise FileNotFoundError("Tesseract is not installed or not in PATH. OCR on PDFs is disabled.")
                    if not shutil.which("pdftoppm"):
                        raise FileNotFoundError("Poppler (pdftoppm) is not installed or not in PATH. OCR on PDFs is disabled.")
                    try:
                        images = convert_from_path(
                            file_path, first_page=page_num, last_page=page_num
                        )
                        if images:
                            ocr_text = pytesseract.image_to_string(images[0])
                            if ocr_text and ocr_text.strip() not in text_content:
                                text_content.append(
                                    f"[OCR from page {page_num}]\n{ocr_text.strip()}"
                                )
                    except Exception as e:
                        logging.warning(f"OCR failed for page {page_num}: {e}")

                if callback:
                    callback()
        logging.info(f"Extracted text from PDF: {file_path}")
        return "\n".join(text_content)
    except Exception as e:
        logging.error(f"Could not read PDF file {file_path}: {e}")
        return None
