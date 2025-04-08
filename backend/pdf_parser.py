from PyPDF2 import PdfReader
from pytesseract import image_to_string
from pdf2image import convert_from_path
import os

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file. Supports both text-based and scanned PDFs.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    text = ""

    try:
        # Attempt to extract text from text-based PDFs
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")

    if not text.strip():
        # If no text is extracted, process as a scanned PDF using OCR
        print("No text found in PDF. Attempting OCR...")
        images = convert_from_path(pdf_path)
        for image in images:
            text += image_to_string(image)

    return text.strip()
