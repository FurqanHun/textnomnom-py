# main.py
import argparse
import logging
import os
import sys
import inquirer
from tqdm import tqdm
from PyPDF2 import PdfReader
from pptx import Presentation

from app.logger_config import setup_logging, clear_log_file
from app.file_processor import process_file, save_text_to_file
from app.web_scraper import scrape_and_save
from app import __version__ as VERSION
from app.config_manager import LOGS

def get_output_path(input_path):
    """Generates the standard output path for a given input file."""
    output_dir = os.path.join(os.path.dirname(input_path), "extracted_texts")
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    return os.path.join(output_dir, f"{base_name}.txt")

def get_total_steps(file_list):
    """Counts the total number of pages/slides in a list of files for the progress bar."""
    total = 0
    print("-> Analyzing files to determine total progress...")
    for file_path in tqdm(file_list, desc="Analyzing files", unit="file", leave=False):
        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext == '.pdf':
                with open(file_path, 'rb') as f:
                    reader = PdfReader(f, strict=False)
                    total += len(reader.pages)
            elif ext == '.pptx':
                prs = Presentation(file_path)
                total += len(prs.slides)
            else:
                total += 1 # Other files count as one step
        except Exception:
            total += 1 # If a file is unreadable, still count it as one step
    return total

def run_interactive_menu():
    """
    Displays an interactive menu for the user to choose an action.
    """
    print("Welcome to TextNomNom Interactive Mode!")

    while True:
        # This is the main menu question
        questions = [
            inquirer.List('action',
                          message="What would you like to do?",
                          choices=[
                              'Process a File or Directory',
                              'Scrape a Web URL',
                              'Clear Log File',
                              'Exit'
                          ])
        ]

        answers = inquirer.prompt(questions)
        # If user presses Ctrl+C on the menu, inquirer returns None
        if not answers:
            raise KeyboardInterrupt

        action = answers['action']

        if action == 'Process a File or Directory':
            # Use standard input() for reliability; it raises KeyboardInterrupt on Ctrl+C
            path = input("[?] Enter the path to the file or directory: ").strip().strip("'\"")

            # If the user just presses Enter, the path is empty, so we loop back
            if not path:
                continue

            if not os.path.exists(path):
                print(f"❌ Error: Path not found: {path}")
                continue

            ocr_q = [inquirer.Confirm('ocr', message="Enable mixed OCR (slower)?", default=False)]
            ocr_answers = inquirer.prompt(ocr_q)
            if not ocr_answers:
                print("\nOperation cancelled.")
                continue
            ocr_mix = ocr_answers['ocr']

            if os.path.isdir(path):
                save_all_q = [inquirer.Confirm('save_all', message="Combine all text into a single file?", default=False)]
                save_all_answers = inquirer.prompt(save_all_q)
                if not save_all_answers:
                    print("\nOperation cancelled.")
                    continue
                save_all = save_all_answers['save_all']

                file_list = [os.path.join(r, f) for r, _, fs in os.walk(path) for f in fs]
                total_steps = get_total_steps(file_list)
                all_texts = []

                with tqdm(total=total_steps, desc="Processing Pages/Slides", unit="step") as pbar:
                    for file_path in file_list:
                        pbar.set_description(f"-> Analyzing {os.path.basename(file_path)}")
                        text = process_file(file_path, ocr_mix=ocr_mix, callback=pbar.update)
                        if text:
                            if save_all:
                                all_texts.append(f"### {file_path} ###\n{text}\n\n")
                            else:
                                output_path = get_output_path(file_path)
                                save_text_to_file(output_path, text)

                if save_all and all_texts:
                    output_file = os.path.join(path, "all_extracted_text.txt")
                    save_text_to_file(output_file, "\n".join(all_texts))
                    print(f"\n✅ All text combined and saved to: {output_file}")

            else: # It's a file
                file_ext = os.path.splitext(path)[1].lower()
                if file_ext in ['.pdf', '.pptx']:
                    total_steps = get_total_steps([path])
                    with tqdm(total=total_steps, desc=f"-> Analyzing {os.path.basename(path)}", unit="step") as pbar:
                        text = process_file(path, ocr_mix=ocr_mix, callback=pbar.update)
                        if text:
                            output_path = get_output_path(path)
                            save_text_to_file(output_path, text)
                else:
                    print(f"Processing file: {path}")
                    text = process_file(path, ocr_mix=ocr_mix)
                    if text:
                        output_path = get_output_path(path)
                        save_text_to_file(output_path, text)

        elif action == 'Scrape a Web URL':
            url = input("[?] Enter the URL to scrape: ").strip().strip("'\"")
            if url: # Only proceed if the user entered something
                scrape_and_save(url)

        elif action == 'Clear Log File':
            clear_log_file()

        elif action == 'Exit':
            # Trigger the main KeyboardInterrupt handler for a single, clean exit message
            raise KeyboardInterrupt

        print("\n" + "="*20 + "\n")

def main():
    """
    Main function to parse arguments or run the interactive menu.
    Returns the mode it ran in ('cli' or 'interactive').
    """
    parser = argparse.ArgumentParser(description="TextNomNom - A versatile text extraction tool.")
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {VERSION}')
    parser.add_argument("path", nargs="?", default=None, help="Path to a file, directory, or a URL.")
    parser.add_argument("--clear-log", action="store_true", help="Clear the log file.")
    parser.add_argument("--debug", action="store_true", help="Enable detailed logging.")
    parser.add_argument("-a", "--save-all", action="store_true", help="Save all output to a single file.")
    parser.add_argument("--ocr", action="store_true", help="Enable OCR for image files.")
    parser.add_argument("--ocr-mix", action="store_true", help="Enable mixed-mode OCR.")
    args = parser.parse_args()

    # Setup logging based on --debug flag OR LOGS config from the start.
    if args.debug or LOGS:
        setup_logging(debug_mode=args.debug)

    # Decide between CLI mode and Interactive mode
    if args.path or args.clear_log:
        if args.clear_log:
            clear_log_file()
            return "cli"

        if args.path.startswith("http"):
            scrape_and_save(args.path)
            return "cli"

        if not os.path.exists(args.path):
            print(f"Error: Path not found: {args.path}")
            return "cli"

        if os.path.isdir(args.path):
            file_list = [os.path.join(r, f) for r, _, fs in os.walk(args.path) for f in fs]
            total_steps = get_total_steps(file_list)
            all_texts = []

            with tqdm(total=total_steps, desc="Processing Pages/Slides", unit="step") as pbar:
                for file_path in file_list:
                    pbar.set_description(f"-> Analyzing {os.path.basename(file_path)}")
                    text = process_file(file_path, args.ocr, args.ocr_mix, callback=pbar.update)
                    if text:
                        if args.save_all:
                            all_texts.append(f"### {file_path} ###\n{text}\n\n")
                        else:
                            output_path = get_output_path(file_path)
                            save_text_to_file(output_path, text)

            if args.save_all and all_texts:
                output_file = os.path.join(args.path, "all_extracted_text.txt")
                save_text_to_file(output_file, "\n".join(all_texts))
                print(f"\n✅ All text combined and saved to: {output_file}")

        else: # It's a file
            file_ext = os.path.splitext(args.path)[1].lower()

            # Check if it's a file type that supports page-by-page progress
            if file_ext in ['.pdf', '.pptx']:
                total_steps = get_total_steps([args.path])
                with tqdm(total=total_steps, desc=f"-> Analyzing {os.path.basename(args.path)}", unit="step") as pbar:
                    text = process_file(args.path, args.ocr, args.ocr_mix, callback=pbar.update)
                    if text:
                        output_path = get_output_path(args.path)
                        save_text_to_file(output_path, text)
            else:
                # For other files (like images), just process without a progress bar
                print(f"Processing file: {args.path}")
                text = process_file(args.path, args.ocr, args.ocr_mix)
                if text:
                    output_path = get_output_path(args.path)
                    save_text_to_file(output_path, text)

        return "cli"
    else:
        run_interactive_menu()
        return "interactive"

if __name__ == "__main__":
    print(f"\nTextNomNom v{VERSION} - 0xQan\n")
    try:
        run_mode = main()
        if run_mode == "cli":
             print("\nExiting...\n")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting.")
        sys.exit(0)
