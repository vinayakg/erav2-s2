# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "fastapi",
#     "uvicorn",
#     "python-multipart",
#     "pillow",
#     "pytesseract",
#     "PyPDF2",
#     "python-docx",
# ]
# ///

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional
import io

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pytesseract
from PIL import Image
import PyPDF2
from docx import Document
import pytesseract
import os

# Set tesseract path explicitly for Ubuntu/Linux
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Verify tesseract is accessible
if not os.path.exists('/usr/bin/tesseract'):
    # Try alternative path
    if os.path.exists('/usr/local/bin/tesseract'):
        pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

app = FastAPI(title="Animal Selector & File Upload API")

# Create uploads directory structure
UPLOAD_BASE_DIR = Path("uploads")
UPLOAD_BASE_DIR.mkdir(exist_ok=True)

# Static files directory (we'll create this to serve the frontend)
STATIC_DIR = Path("static")
STATIC_DIR.mkdir(exist_ok=True)


def get_upload_dir() -> Path:
    """Create and return today's upload directory"""
    today = datetime.now().strftime("%Y-%m-%d")
    upload_dir = UPLOAD_BASE_DIR / today
    upload_dir.mkdir(exist_ok=True)
    return upload_dir


def generate_unique_filename(original_filename: str) -> str:
    """Generate unique filename with UUID prefix"""
    unique_id = str(uuid.uuid4())[:8]
    return f"{unique_id}_{original_filename}"


def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract text from image using OCR"""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"OCR extraction failed: {str(e)}"


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text_parts = []
        
        for page in pdf_reader.pages:
            text_parts.append(page.extract_text())
        
        return "\n".join(text_parts).strip()
    except Exception as e:
        return f"PDF extraction failed: {str(e)}"


def extract_text_from_docx(docx_bytes: bytes) -> str:
    """Extract text from Word document"""
    try:
        doc = Document(io.BytesIO(docx_bytes))
        text_parts = []
        
        for paragraph in doc.paragraphs:
            text_parts.append(paragraph.text)
        
        return "\n".join(text_parts).strip()
    except Exception as e:
        return f"DOCX extraction failed: {str(e)}"


def extract_text_from_file(file_bytes: bytes, content_type: str, filename: str) -> str:
    """Extract text based on file type"""
    filename_lower = filename.lower()
    
    # Text files
    if content_type.startswith('text/') or filename_lower.endswith(('.txt', '.md', '.csv', '.json', '.xml', '.html')):
        try:
            return file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return file_bytes.decode('latin-1')
            except:
                return "Text extraction failed: Unable to decode file"
    
    # Images
    elif content_type.startswith('image/') or filename_lower.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')):
        return extract_text_from_image(file_bytes)
    
    # PDFs
    elif content_type == 'application/pdf' or filename_lower.endswith('.pdf'):
        return extract_text_from_pdf(file_bytes)
    
    # Word documents
    elif (content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' 
          or filename_lower.endswith('.docx')):
        return extract_text_from_docx(file_bytes)
    
    else:
        return f"Unsupported file type: {content_type}. No text extraction available."


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 Bytes"
    
    size_names = ["Bytes", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle file upload and text extraction"""
    try:
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Generate unique filename and save path
        unique_filename = generate_unique_filename(file.filename or "unknown_file")
        upload_dir = get_upload_dir()
        file_path = upload_dir / unique_filename
        
        # Save file to disk
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Extract text from file
        extracted_text = extract_text_from_file(
            file_content, 
            file.content_type or "", 
            file.filename or ""
        )
        
        # Prepare response
        response_data = {
            "status": "success",
            "message": f"File uploaded and processed successfully",
            "filename": unique_filename,
            "type": file.content_type or "unknown",
            "size": format_file_size(file_size),
            "extracted_text": extracted_text
        }
        
        return response_data
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail={
                "status": "error",
                "message": f"File processing failed: {str(e)}",
                "filename": "",
                "type": "",
                "size": "",
                "extracted_text": ""
            }
        )


@app.get("/")
async def read_index():
    """Serve the main HTML page"""
    return FileResponse('static/index.html')


# Mount static files (we'll put our HTML here)
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
