import os
import sys
import logging
import subprocess
from PyPDF2 import PdfReader
from pptx import Presentation
import shutil

# Configure logging
LOG_FILE = "file_processing.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()  # Also log to console
    ]
)

def extract_text_from_pdf(file_path):
    """Extract text from each page of the PDF."""
    pdf_text = []
    try:
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pdf_text.append(text)
        logging.info(f"Extracted text from PDF: {file_path}")
    except Exception as e:
        logging.error(f"Error reading the PDF file: {e}")
        return None
    return "\n".join(pdf_text)

def convert_ppt_to_pptx(ppt_path):
    """Convert .ppt to .pptx using external tools."""
    temp_dir = os.path.dirname(ppt_path)
    temp_filename = f"temp_{os.path.basename(ppt_path)}x"
    pptx_path = os.path.join(temp_dir, temp_filename)

    if sys.platform == 'win32':
        try:
            import win32com.client
            powerpoint = win32com.client.Dispatch("PowerPoint.Application")
            # powerpoint.Visible = False
            deck = powerpoint.Presentations.Open(ppt_path)
            deck.SaveAs(pptx_path, 24)  # 24 = .pptx format
            deck.Close()
            powerpoint.Quit()
            logging.info(f"Successfully converted .ppt to .pptx using PowerPoint: {pptx_path}")
            return pptx_path
        except Exception as e:
            logging.error(f"PowerPoint automation failed: {e}")
    else:
        converters = [
            {
                "name": "soffice",
                "cmd": ["soffice", "--headless", "--convert-to", "pptx", "--outdir", temp_dir, ppt_path],
            },
            {
                "name": "unoconv",
                "cmd": ["unoconv", "-f", "pptx", "-o", temp_dir, ppt_path],
            }
        ]

        for converter in converters:
            if shutil.which(converter["cmd"][0]):
                try:
                    logging.info(f"Attempting .ppt to .pptx conversion using {converter['name']}...")
                    result = subprocess.run(converter["cmd"], capture_output=True, text=True)
                    if result.returncode == 0 and os.path.exists(pptx_path):
                        logging.info(f"Successfully converted .ppt to .pptx: {pptx_path}")
                        return pptx_path
                    else:
                        logging.warning(f"{converter['name']} failed. Output: {result.stderr.strip()}")
                except Exception as e:
                    logging.error(f"{converter['name']} conversion failed: {e}")
        logging.error("No conversion tools succeeded. Please convert the .ppt manually.")
        return None

def extract_text_from_pptx(file_path):
    """Extract text from PowerPoint presentation."""
    pptx_text = []
    try:
        prs = Presentation(file_path)
        for slide_number, slide in enumerate(prs.slides, 1):
            slide_text = []
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    slide_text.append(shape.text.strip())
            if slide_text:
                pptx_text.append(f"[Slide {slide_number}]\n" + "\n".join(slide_text))
        logging.info(f"Extracted text from PowerPoint: {file_path}")
    except Exception as e:
        logging.error(f"Error reading the PowerPoint file: {e}")
        return None
    return "\n\n".join(pptx_text)

def convert_pptx_to_pdf(pptx_path):
    """Convert .pptx to .pdf using external tools."""
    temp_dir = os.path.dirname(pptx_path)
    pdf_path = os.path.splitext(pptx_path)[0] + ".pdf"

    if sys.platform == 'win32':
        try:
            import win32com.client
            powerpoint = win32com.client.Dispatch("PowerPoint.Application")
            # powerpoint.Visible = False
            presentation = powerpoint.Presentations.Open(pptx_path)
            presentation.SaveAs(pdf_path, FileFormat=32)  # 32 = ppSaveAsPDF
            presentation.Close()
            powerpoint.Quit()
            logging.info(f"Successfully converted .pptx to .pdf: {pdf_path}")
            return pdf_path
        except Exception as e:
            logging.error(f"PowerPoint automation failed: {e}")
            return None
    else:
        converters = [
            {
                "name": "soffice",
                "cmd": ["soffice", "--headless", "--convert-to", "pdf", "--outdir", temp_dir, pptx_path],
            },
            {
                "name": "unoconv",
                "cmd": ["unoconv", "-f", "pdf", "-o", temp_dir, pptx_path],
            }
        ]

        for converter in converters:
            if shutil.which(converter["cmd"][0]):
                try:
                    logging.info(f"Attempting .pptx to .pdf conversion using {converter['name']}...")
                    result = subprocess.run(converter["cmd"], capture_output=True, text=True)
                    if result.returncode == 0 and os.path.exists(pdf_path):
                        logging.info(f"Successfully converted .pptx to .pdf: {pdf_path}")
                        return pdf_path
                    else:
                        logging.warning(f"{converter['name']} failed. Output: {result.stderr.strip()}")
                except Exception as e:
                    logging.error(f"{converter['name']} conversion failed: {e}")
        logging.error("No conversion tools succeeded. Please convert the .pptx manually.")
        return None

def extract_text_from_file(file_path):
    """Extract text based on file type."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".pptx":
        return extract_text_from_pptx(file_path)
    elif ext == ".ppt":
        logging.info(".ppt file detected. Attempting conversion...")
        pptx_path = convert_ppt_to_pptx(file_path)
        if pptx_path:
            return extract_text_from_pptx(pptx_path)
        else:
            logging.error("Failed to process .ppt file.")
            return None
    else:
        logging.error(f"Unsupported file type: {ext}")
        return None

def save_to_txt(output_path, text):
    """Save extracted text to a .txt file."""
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(text)
        logging.info(f"Text successfully saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to save text to {output_path}: {e}")

def process_directory(directory_path, save_all=False, output_file=None):
    """Process all supported files in the directory recursively."""
    all_text = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(".txt") and "extracted_texts" in root:
                           continue

            file_path = os.path.join(root, file)
            logging.info(f"Processing file: {file_path}")
            text = extract_text_from_file(file_path)
            if text:
                if save_all:
                    all_text.append(f"### {file_path} ###\n{text}\n\n")
                else:
                    # output_path = os.path.splitext(file_path)[0] + ".txt"
                    output_path = os.path.join(os.path.dirname(file_path), "extracted_texts", os.path.splitext(os.path.basename(file_path))[0] + ".txt")
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    save_to_txt(output_path, text)
    if save_all and output_file:
        save_to_txt(output_file, "\n".join(all_text))

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: python main.py <file_or_directory_path> [options]")
        print("Options:")
        print("  -h, --help            Show this help message and exit.")
        print("  -a                    Save all extracted text from files in the directory to a single text file (all_extracted_text.txt).")
        print("  --convert pdf         Convert PowerPoint (.ppt or .pptx) to PDF.")

        sys.exit(1)

    path = sys.argv[1]
    save_all = "-a" in sys.argv
    convert_pdf = "--convert" in sys.argv and "pdf" in sys.argv

    if not os.path.exists(path):
        logging.error(f"Path not found: {path}")
        sys.exit(1)

    # output_file = "all_extracted_text.txt" if save_all else None
    # output_file = os.path.join(path, "all_extracted_text.txt") if save_all else None
    output_file = os.path.join(os.path.dirname(path), "extracted_texts", "all_extracted_text.txt")

    if convert_pdf:
        # Convert to PDF if --convert pdf is passed
        if path.lower().endswith(('.ppt', '.pptx')):
            logging.info(f"Converting PowerPoint file to PDF: {path}")
            if path.lower().endswith('.ppt'):
                # Convert .ppt to .pptx first if it's a .ppt file
                pptx_path = convert_ppt_to_pptx(path)
                if pptx_path:
                    path = pptx_path
            pdf_path = convert_pptx_to_pdf(path)
            if pdf_path:
                logging.info(f"Converted to PDF: {pdf_path}")
                sys.exit(0)
            else:
                logging.error(f"Conversion failed for: {path}")
                sys.exit(1)
        else:
            logging.error("Invalid file type. Only .ppt or .pptx files can be converted to PDF.")
            sys.exit(1)

    if os.path.isdir(path):
        logging.info(f"Processing directory: {path}")
        output_folder = os.path.join(path, "extracted_texts")
        os.makedirs(output_folder, exist_ok=True)
        process_directory(path, save_all, output_file)
    else:
        logging.info(f"Processing single file: {path}")
        text = extract_text_from_file(path)
        if text:
            if save_all:
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                save_to_txt(output_file, text)
            else:
                # output_path = os.path.splitext(path)[0] + ".txt"
                output_path = os.path.join(os.path.dirname(path), "extracted_texts", os.path.splitext(os.path.basename(path))[0] + ".txt")
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                save_to_txt(output_path, text)

if __name__ == "__main__":
    print("\nText extraction and conversion tool - 0xQan\n")
    main()
