import requests
from io import BytesIO
import PyPDF2
from docx import Document as DocxDocument
import pytesseract
from PIL import Image
from typing import List, Dict
import email
from email import policy
from email.parser import BytesParser
from urllib.parse import urlparse
import os

class DocumentProcessor:
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def process_document_from_url(self, url: str) -> List[Dict]:
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError("Failed to download document")

        content = BytesIO(response.content)
        # Get file extension from the path only (ignoring query params)
        path = urlparse(url).path
        _, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext == '.pdf':
            text = self._extract_text_from_pdf(content)
        elif ext == '.docx':
            text = self._extract_text_from_docx(content)
        elif ext == '.eml':
            text = self._extract_text_from_email(content)
        else:
            raise ValueError("Unsupported document format. Supported: .pdf, .docx, .eml")

        return self._chunk_text(text)

    def _extract_text_from_pdf(self, content: BytesIO) -> str:
        reader = PyPDF2.PdfReader(content)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
        # Fallback to OCR if text is empty (scanned PDF)
        if not text.strip():
            text = self._ocr_from_pdf(content)
        return text

    def _extract_text_from_docx(self, content: BytesIO) -> str:
        doc = DocxDocument(content)
        return "\n".join([para.text for para in doc.paragraphs])

    def _extract_text_from_email(self, content: BytesIO) -> str:
        msg = BytesParser(policy=policy.default).parse(content)
        subject = msg['subject'] or ""
        sender = msg['from'] or ""
        if msg.is_multipart():
            body = ""
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body += part.get_content().strip() + "\n"
        else:
            body = msg.get_content().strip()
        email_text = f"Subject: {subject}\nFrom: {sender}\nBody:\n{body}"
        return email_text

    def _ocr_from_pdf(self, content: BytesIO) -> str:
        # To implement OCR, you would need pdf2image and pytesseract.
        # This is a placeholder for actual OCR integration.
        return ""

    def _chunk_text(self, text: str) -> List[Dict]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk = {
                "text": ' '.join(chunk_words),
                "chunk_id": len(chunks),
                "start_index": i,
                "end_index": min(i + self.chunk_size, len(words))
            }
            chunks.append(chunk)
        return chunks
