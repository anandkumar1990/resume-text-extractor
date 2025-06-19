# Resume Text Extractor

A Python project for extracting text from resumes in PDF, DOCX, DOC, and TXT formats. Supports OCR for scanned documents and embedded images.

## Features

- Extracts text from PDF, DOCX, DOC, and TXT files
- OCR support for scanned PDFs and images in DOCX
- Batch processing of resume files
- Flask API for file upload and extraction

## Requirements

- Python 3.7+
- See `requirements.txt` for dependencies

## Installation

```sh
git clone https://github.com/anandkumar1990/resume-text-extractor.git
cd resume-text-extractor
pip install -r requirements.txt
```

## Usage

### Run as Flask API

```sh
python app.py
```

### API Endpoints

#### 1. `/extract` (POST)
- Upload one or more files (PDF, DOCX, DOC, TXT) as form-data with the key `files`.
- Returns extracted text for each file.

#### 2. `/process_files` (POST)
- Triggers batch processing of all files in the configured input directory.
- Returns a summary of processed and skipped files.

### Batch Process Files (CLI)

Set mode to CLI and run:

```sh
set RUN_MODE=cli
python app.py
```

## Project Structure

- `app.py` - Flask API endpoints
- `text_extraction.py` - Extraction and processing logic
- `requirements.txt` - Python dependencies

## License

MIT License
