# app/file_handlers/pdf_handler.py

import logging
import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.config_manager import MAX_OCR_WORKERS

# Limit Tesseract's internal OpenMP threading to prevent CPU saturation
os.environ["OMP_THREAD_LIMIT"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"


def page_has_images(page):
    """Checks if a PDF page contains any image objects."""
    try:
        resources = page.get('/Resources')
        if hasattr(resources, 'get_object'):
            resources = resources.get_object()
        if not resources:
            return False
            
        xobject = resources.get('/XObject')
        if hasattr(xobject, 'get_object'):
            xobject = xobject.get_object()
        if not xobject:
            return False
            
        for key in xobject:
            obj = xobject[key]
            if hasattr(obj, 'get_object'):
                obj = obj.get_object()
            if obj.get('/Subtype') == '/Image':
                return True
    except Exception:
        pass
    return False


def is_duplicate(standard_text, ocr_text):
    """Checks if the OCR text is substantially similar or already contained in standard text."""
    def normalize(t):
        return "".join(c for c in t.lower() if c.isalnum())
    norm_std = normalize(standard_text)
    norm_ocr = normalize(ocr_text)
    if not norm_ocr:
        return True
    if norm_ocr in norm_std:
        return True
    return False


def extract_text_from_pdf(file_path, trigger_ocr=False, ocr_mix=False, callback=None):
    """Extracts text from a PDF, with an option for OCR."""
    text_content = []
    try:
        # Validate external dependencies before starting OCR
        if trigger_ocr or ocr_mix:
            if not shutil.which("tesseract"):
                raise FileNotFoundError("Tesseract is not installed or not in PATH. OCR on PDFs is disabled.")
            if not shutil.which("pdftoppm"):
                raise FileNotFoundError("Poppler (pdftoppm) is not installed or not in PATH. OCR on PDFs is disabled.")

        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            num_pages = len(reader.pages)
            
            # Extract standard text content
            standard_texts = {}
            pages_to_ocr = []
            
            for page_num in range(1, num_pages + 1):
                page = reader.pages[page_num - 1]
                text = page.extract_text() or ""
                if text.strip():
                    standard_texts[page_num] = text
                
                if trigger_ocr or ocr_mix:
                    # Queue page for OCR if forced, or if mixed-mode finds a scanned page or embedded image
                    if trigger_ocr or (not text.strip()) or page_has_images(page):
                        pages_to_ocr.append(page_num)

            # Process queued OCR pages concurrently
            ocr_results = {}
            if (trigger_ocr or ocr_mix) and pages_to_ocr:
                max_workers = MAX_OCR_WORKERS
                
                def process_page_ocr(p_num):
                    try:
                        images = convert_from_path(
                            file_path, first_page=p_num, last_page=p_num
                        )
                        if images:
                            ocr_text = pytesseract.image_to_string(images[0])
                            return p_num, ocr_text.strip()
                    except Exception as e:
                        logging.warning(f"OCR failed for page {p_num}: {e}")
                    return p_num, ""

                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = {executor.submit(process_page_ocr, p_num): p_num for p_num in pages_to_ocr}
                    for future in as_completed(futures):
                        p_num, ocr_text = future.result()
                        if ocr_text:
                            ocr_results[p_num] = ocr_text
                        if callback:
                            callback()
                
                # Update progress for pages that skipped OCR
                skipped_pages = num_pages - len(pages_to_ocr)
                if callback and skipped_pages > 0:
                    for _ in range(skipped_pages):
                        callback()
            else:
                # Update progress for all pages when OCR is disabled
                if callback:
                    for _ in range(num_pages):
                        callback()

            # Merge standard and OCR texts in page order
            for page_num in range(1, num_pages + 1):
                std_text = standard_texts.get(page_num, "").strip()
                ocr_text = ocr_results.get(page_num, "").strip()
                
                page_texts = []
                if std_text:
                    page_texts.append(std_text)
                
                if ocr_text:
                    # Skip OCR text if it duplicates standard text content
                    if not std_text or not is_duplicate(std_text, ocr_text):
                        page_texts.append(f"[OCR from page {page_num}]\n{ocr_text}")
                
                if page_texts:
                    text_content.append("\n".join(page_texts))

        logging.info(f"Extracted text from PDF: {file_path}")
        return "\n".join(text_content)
    except Exception as e:
        logging.error(f"Could not read PDF file {file_path}: {e}")
        return None
