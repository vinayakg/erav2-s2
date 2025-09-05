# Animal Selector & File Upload Application

A web application with animal image selection and file upload functionality with text extraction capabilities.

## Features

- **Animal Selection**: Choose from Cat, Dog, or Elephant with live external images
- **File Upload**: Upload any file type with automatic text extraction
- **Text Extraction Support**:
  - Images (OCR using Tesseract)
  - PDF documents
  - Word documents (.docx)
  - Plain text files
- **Smart Display**: Uploaded images shown with extracted text in readable format
- **Auto-clearing**: Fresh uploads clear previous selections

## Project Structure

```
animal-file-upload/
├── main.py                 # FastAPI backend
├── static/
│   └── index.html         # Frontend HTML (create this directory)
├── uploads/               # File storage (auto-created)
│   └── YYYY-MM-DD/       # Date-organized folders
├── pyproject.toml         # Project configuration
└── README.md             # This file
```

## Prerequisites

### 1. Install uv (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # or restart terminal
```

### 2. Install Tesseract OCR (Required for image text extraction)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-eng
```

**CentOS/RHEL/Fedora:**
```bash
sudo yum install tesseract tesseract-langpack-eng
# or for newer versions:
sudo dnf install tesseract tesseract-langpack-eng
```

**Verify Tesseract installation:**
```bash
tesseract --version
```

## Setup Instructions

### 1. Create Project Directory
```bash
mkdir animal-file-upload
cd animal-file-upload
```

### 2. Create Files
Create the following files in your project directory:

- Copy the `main.py` content into `main.py`
- Copy the `pyproject.toml` content into `pyproject.toml`
- Create `static/` directory and copy the HTML content into `static/index.html`

```bash
mkdir static
# Copy the HTML content into static/index.html
```

### 3. Initialize with uv
```bash
uv init --no-readme
uv add fastapi uvicorn python-multipart pillow pytesseract PyPDF2 python-docx
```

Or simply use the existing pyproject.toml:
```bash
uv sync
```

## Running the Application

### Development Mode (with auto-reload)
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### Using Project Scripts
```bash
# Development
uv run start

# Production  
uv run start-prod
```

## Access the Application

Open your browser and navigate to:
```
http://localhost:8000
```

Or if running on a remote Linux VM:
```
http://YOUR_VM_IP:8000
```

## API Endpoints

### GET /
- Serves the main HTML interface

### POST /api/upload
- Accepts file uploads via multipart/form-data
- Returns JSON with file info and extracted text
- Response format:
```json
{
  "status": "success",
  "message": "File uploaded and processed successfully",
  "filename": "unique_id_originalname.ext",
  "type": "application/pdf",
  "size": "1.2 MB",
  "extracted_text": "Extracted content here..."
}
```

## File Storage

Uploaded files are automatically organized by date:
```
uploads/
├── 2025-01-15/
│   ├── abc123_document.pdf
│   └── def456_image.jpg
├── 2025-01-16/
│   └── ghi789_report.docx
```

## Supported File Types

- **Images**: JPG, JPEG, PNG, BMP, TIFF, GIF (OCR text extraction)
- **Documents**: PDF, DOCX (native text extraction)
- **Text Files**: TXT, MD, CSV, JSON, XML, HTML (direct text reading)

## Troubleshooting

### Tesseract Issues
```bash
# Check if tesseract is in PATH
which tesseract

# Install additional language packs if needed
sudo apt install tesseract-ocr-all  # Ubuntu
```

### Port Already in Use
```bash
# Check what's using port 8000
sudo lsof -i :8000

# Use a different port
uv run uvicorn main:app --host 0.0.0.0 --port 8080
```

### Permission Issues
```bash
# Make sure uploads directory is writable
chmod 755 uploads/
```

## Git Setup

### Initialize Repository
```bash
# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: Animal selector and file upload app"
```

### Push to GitHub/GitLab
```bash
# Add remote repository (replace with your repo URL)
git remote add origin https://github.com/yourusername/animal-file-upload.git

# Push to remote
git push -u origin main
```

### Create Repository on GitHub
1. Go to [GitHub](https://github.com) and create a new repository
2. Name it `animal-file-upload`
3. Don't initialize with README (we already have one)
4. Copy the repository URL and use it in the `git remote add` command above

## Development

### Code Formatting
```bash
uv run black main.py
uv run isort main.py
```

### Linting
```bash
uv run flake8 main.py
```

### Git Workflow
```bash
# Make changes, then:
git add .
git commit -m "Description of changes"
git push
```

## Security Notes

- Files are stored locally on the server
- No authentication implemented (add as needed)
- Consider file size limits for production use
- Validate file types as needed for your use case
- **Note**: `uploads/` directory is in `.gitignore` - uploaded files won't be committed
