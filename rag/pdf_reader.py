from pypdf import PdfReader


def extract_pdf_pages(pdf_file):
    if hasattr(pdf_file, 'seek'):
        pdf_file.seek(0)
    reader = PdfReader(pdf_file)
    if reader.is_encrypted and not reader.decrypt(''):
        raise ValueError('Password-protected PDFs are not supported. Upload an unlocked copy.')
    pages = [{'page': i + 1, 'text': page.extract_text() or ''}
             for i, page in enumerate(reader.pages)]
    if not any(page['text'].strip() for page in pages):
        raise ValueError('This PDF has no extractable text. Run OCR before uploading it.')
    return pages


def extract_pdf_text(pdf_file):
    return '\n\n'.join(page['text'] for page in extract_pdf_pages(pdf_file))
