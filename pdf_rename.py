import os
import re
import time
import watchdog.events
import watchdog.observers
from PyPDF2 import PdfReader

class PDFEventHandler(watchdog.events.PatternMatchingEventHandler):
    def on_created(self, event):
        if event.src_path.lower().endswith('.pdf'):
            print("New PDF file detected:", event.src_path)
            self.rename_pdf(event.src_path)

    def rename_pdf(self, pdf_path):
        print("Renaming PDF:", pdf_path)
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            # Extract text from the first page
            first_page_text = reader.pages[0].extract_text()
            print("First page text:", first_page_text)
            # Use regex to find the first heading sentence
            main_heading_match = re.search(r'^[^.]*\.', first_page_text, re.MULTILINE)
            if main_heading_match:
                main_heading = main_heading_match.group(0).strip()
                new_filename = f"{main_heading}.pdf"
                new_filepath = os.path.join(os.path.dirname(pdf_path), new_filename)
                print("New filename:", new_filename)
                print("New filepath:", new_filepath)
                os.rename(pdf_path, new_filepath)
                print("PDF renamed successfully.")
            else:
                print("Main heading not found. PDF not renamed.")

def start_observer(folder_to_watch):
    patterns = ["*.pdf"]
    event_handler = PDFEventHandler(patterns=patterns)
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()
    print("PDF renaming script started. Monitoring folder:", folder_to_watch)
    return observer
