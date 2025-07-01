# app/file_handlers/image_handler.py
import logging
import shutil
from PIL import Image
import pytesseract

def extract_text_from_image(file_path):
    """Extracts text from an image file using Tesseract OCR."""
    # Proactively check for Tesseract
    if not shutil.which("tesseract"):
        raise FileNotFoundError("Tesseract is not installed or is not in your system's PATH. Cannot perform OCR on images.")

    try:
        text = pytesseract.image_to_string(Image.open(file_path))
        logging.info(f"Successfully extracted text from image: {file_path}")
        return text.strip()
    except Exception as e:
        logging.error(f"Could not process image file {file_path}: {e}")
        return None
