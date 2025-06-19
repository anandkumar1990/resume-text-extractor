from flask import Flask, request, jsonify
import os
from text_extraction import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt,
    convert_doc_to_docx,
    extract_text_from_docx,
    clean_text,
    process_resume,
    batch_process_files,
    INPUT_DIR,
    OUTPUT_DIR
)

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract():
    if 'files' not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    results = []
    for file in request.files.getlist("files"):
        filename = file.filename
        ext = os.path.splitext(filename)[1].lower()
        content = file.read()

        try:
            if ext == ".pdf":
                text = extract_text_from_pdf(content)
            elif ext == ".docx":
                text = extract_text_from_docx(content)
            elif ext == ".txt":
                text = extract_text_from_txt(content)
            elif ext == ".doc":
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix=".doc", mode="wb") as tmp_doc:
                    tmp_doc.write(content)
                    tmp_doc_path = tmp_doc.name
                docx_path = convert_doc_to_docx(tmp_doc_path)
                text = ""
                if docx_path and os.path.exists(docx_path):
                    with open(docx_path, "rb") as f:
                        docx_bytes = f.read()
                    text = extract_text_from_docx(docx_bytes)
                    os.unlink(docx_path)
                os.unlink(tmp_doc_path)
            else:
                return jsonify({"error": f"Unsupported file type: {filename}"}), 400

            results.append({
                "filename": filename,
                "full_text": clean_text(text)
            })
        except Exception as e:
            return jsonify({"error": f"Failed to process {filename}: {str(e)}"}), 500

    return jsonify(results), 200

@app.route("/process_files", methods=["POST"])
def process_files_api():
    result = batch_process_files(INPUT_DIR, OUTPUT_DIR)
    return jsonify(result), 200

if __name__ == "__main__":
    mode = os.environ.get("RUN_MODE", "api")
    if mode == "api":
        app.run(debug=True)
    elif mode == "cli":
        from text_extraction import extract_all_resumes
        extract_all_resumes(INPUT_DIR, OUTPUT_DIR)
