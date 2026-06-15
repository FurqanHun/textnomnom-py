# app/file_handlers/pptx_handler.py

import io
import logging
import os
from pptx import Presentation
from PIL import Image
import pytesseract
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.config_manager import MAX_OCR_WORKERS

# Limit Tesseract's internal OpenMP threading to prevent CPU saturation
os.environ["OMP_THREAD_LIMIT"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"


def extract_text_from_pptx(file_path, trigger_ocr=False, ocr_mix=False, callback=None):
    """Extracts text from a .pptx file, with an option for OCR."""
    text_content = []
    try:
        prs = Presentation(file_path)
        
        slide_data = {}
        ocr_tasks = []
        
        for slide_num, slide in enumerate(prs.slides, 1):
            slide_data[slide_num] = []
            for shape_idx, shape in enumerate(slide.shapes):
                if hasattr(shape, "text") and shape.text.strip():
                    slide_data[slide_num].append({
                        'type': 'text',
                        'content': shape.text.strip()
                    })
                elif (trigger_ocr or ocr_mix) and hasattr(shape, "image"):
                    try:
                        image_bytes = shape.image.blob
                        ocr_tasks.append((slide_num, shape_idx, image_bytes))
                        slide_data[slide_num].append({
                            'type': 'image',
                            'shape_idx': shape_idx,
                            'content': ''
                        })
                    except Exception as e:
                        logging.warning(f"Failed to access image on slide {slide_num}: {e}")

        ocr_results = {}
        if ocr_tasks:
            max_workers = MAX_OCR_WORKERS
            
            def process_image_ocr(task):
                slide_num, shape_idx, img_bytes = task
                try:
                    ocr_text = pytesseract.image_to_string(
                        Image.open(io.BytesIO(img_bytes))
                    )
                    return (slide_num, shape_idx), ocr_text.strip()
                except Exception as e:
                    logging.warning(f"OCR on slide {slide_num} shape {shape_idx} failed: {e}")
                return (slide_num, shape_idx), ""

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(process_image_ocr, task): task for task in ocr_tasks}
                for future in as_completed(futures):
                    key, ocr_text = future.result()
                    if ocr_text:
                        ocr_results[key] = ocr_text

        for slide_num, slide in enumerate(prs.slides, 1):
            slide_text = []
            components = slide_data.get(slide_num, [])
            for comp in components:
                if comp['type'] == 'text':
                    slide_text.append(comp['content'])
                elif comp['type'] == 'image':
                    key = (slide_num, comp['shape_idx'])
                    ocr_text = ocr_results.get(key, '')
                    if ocr_text:
                        slide_text.append(f"[OCR from Slide {slide_num}]\n{ocr_text}")
            
            if slide_text:
                text_content.append(f"[Slide {slide_num}]\n" + "\n".join(slide_text))
            
            if callback:
                callback()

        logging.info(f"Extracted text from PowerPoint: {file_path}")
        return "\n\n".join(text_content)
    except Exception as e:
        logging.error(f"Could not read PowerPoint file {file_path}: {e}")
        return None
