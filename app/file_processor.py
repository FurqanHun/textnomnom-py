# app/file_processor.py
import os
import sys
import logging
from PIL import Image

from app.file_handlers.pdf_handler import extract_text_from_pdf
from app.file_handlers.pptx_handler import extract_text_from_pptx
from app.file_handlers.image_handler import extract_text_from_image
from app.file_handlers.conversions import convert_ppt_to_pptx

def save_text_to_file(output_path, text):
    """Saves the extracted text to a .txt file."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✔ Successfully saved output to: {output_path}")
        logging.info(f"Text successfully saved to {output_path}")
    except Exception as e:
        print(f"❌ Error saving text to {output_path}: {e}")
        logging.error(f"Failed to save text to {output_path}: {e}")

def process_file(file_path, trigger_ocr=False, ocr_mix=False, callback=None):
    """
    Selects the correct handler to extract text from a file, with error handling.
    """
    try:
        # --- This is the main dispatch logic ---
        ext = os.path.splitext(file_path)[1].lower()
        logging.info(f"Dispatching file for processing: {file_path}")

        if ext == ".pdf":
            return extract_text_from_pdf(file_path, trigger_ocr, ocr_mix, callback=callback)
        elif ext == ".pptx":
            return extract_text_from_pptx(file_path, trigger_ocr, ocr_mix, callback=callback)
        elif ext == ".ppt":
            pptx_path = convert_ppt_to_pptx(file_path)
            if pptx_path:
                return extract_text_from_pptx(pptx_path, trigger_ocr, ocr_mix, callback=callback)
            return None
        elif ext in Image.registered_extensions() and (trigger_ocr or ocr_mix):
            text = extract_text_from_image(file_path)
            if callback: callback()
            return text
        else:
            logging.warning(f"Unsupported file type for processing: {ext}, skipping.")
            if callback: callback()
            return None

    except FileNotFoundError as e:
        # --- Catch the specific error for missing dependencies ---
        print(f"\n❌ Dependency Error: {e}", file=sys.stderr)
        # We need to tell the progress bar this file is "done" so it doesn't stall.
        if callback:
            # For a file-by-file progress bar, a single update is fine. For a
            # page-by-page bar, this prevents a stall but won't be perfectly accurate.
            callback()
        return None

    except Exception as e:
        # ---Catch any other unexpected errors during processing ---
        print(f"\n❌ An unexpected error occurred while processing {os.path.basename(file_path)}.", file=sys.stderr)
        logging.error(f"Error processing {file_path}: {e}")
        if callback:
            callback()
        return None
