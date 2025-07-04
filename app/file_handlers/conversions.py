# app/file_handlers/conversions.py

import logging
import os
import subprocess
import sys
import shutil


def convert_ppt_to_pptx(ppt_path):
    """Converts a .ppt file to .pptx using available tools."""
    pptx_path = os.path.splitext(ppt_path)[0] + ".pptx"
    temp_dir = os.path.dirname(ppt_path)

    # --- Logic for Windows ---
    if sys.platform == "win32":
        try:
            # Import is placed here to avoid errors on non-Windows systems
            import win32com.client
            powerpoint = win32com.client.Dispatch("PowerPoint.Application")
            deck = powerpoint.Presentations.Open(ppt_path)
            # Format 24 corresponds to .pptx
            deck.SaveAs(pptx_path, 24)
            deck.Close()
            powerpoint.Quit()
            logging.info("Successfully converted .ppt to .pptx using PowerPoint.")
            return pptx_path
        except Exception as e:
            logging.error(f"Windows PowerPoint automation failed: {e}")
            raise FileNotFoundError(f"Could not convert {os.path.basename(ppt_path)}. Ensure Microsoft PowerPoint is installed.")

    # --- Logic for Linux/macOS ---
    if not shutil.which("soffice"):
        raise FileNotFoundError("LibreOffice is not installed or 'soffice' is not in your system's PATH. Cannot convert .ppt files.")

    try:
        cmd = ["soffice", "--headless", "--convert-to", "pptx", "--outdir", temp_dir, ppt_path]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        if os.path.exists(pptx_path):
            logging.info(f"Converted {ppt_path} to {pptx_path} using LibreOffice.")
            return pptx_path
        else:
            raise RuntimeError("LibreOffice conversion finished without creating an output file.")
    except (subprocess.CalledProcessError, FileNotFoundError, RuntimeError) as e:
        logging.error(f"LibreOffice conversion failed: {e}")

    # If all methods fail
    logging.error(f"No suitable tool could convert .ppt file: {ppt_path}")
    return None


def convert_pptx_to_pdf(pptx_path):
    """Converts a .pptx file to .pdf using available tools."""
    pdf_path = os.path.splitext(pptx_path)[0] + ".pdf"
    temp_dir = os.path.dirname(pptx_path)

    # --- Logic for Windows ---
    if sys.platform == "win32":
        try:
            import win32com.client
            powerpoint = win32com.client.Dispatch("PowerPoint.Application")
            # Open presentation without a window
            presentation = powerpoint.Presentations.Open(pptx_path, WithWindow=False)
            # FileFormat 32 corresponds to PDF
            presentation.SaveAs(pdf_path, 32)
            presentation.Close()
            powerpoint.Quit()
            logging.info("Successfully converted .pptx to .pdf using PowerPoint.")
            return pdf_path
        except Exception as e:
            logging.error(f"Windows PowerPoint automation failed: {e}")
            raise FileNotFoundError(f"Could not convert {os.path.basename(pptx_path)}. Ensure Microsoft PowerPoint is installed.")

    # --- Logic for Linux/macOS ---
    if not shutil.which("soffice"):
        raise FileNotFoundError("LibreOffice is not installed or 'soffice' is not in your system's PATH. Cannot convert .pptx files.")

    try:
        cmd = ["soffice", "--headless", "--convert-to", "pdf", "--outdir", temp_dir, pptx_path]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        if os.path.exists(pdf_path):
            logging.info(f"Converted {pptx_path} to {pdf_path} using LibreOffice.")
            return pdf_path
        else:
            raise RuntimeError("LibreOffice conversion finished without creating an output file.")
    except (subprocess.CalledProcessError, FileNotFoundError, RuntimeError) as e:
        logging.error(f"LibreOffice conversion failed: {e}")

    logging.error(f"No suitable tool could convert .pptx file: {pptx_path}")
    return None
