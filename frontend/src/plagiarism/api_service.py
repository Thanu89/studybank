import os
import json
from pdf_ocr import convert_pdf_txt
from plagiarism_check import plag_check
from werkzeug.utils import secure_filename
from fastapi import FastAPI
from fastapi import File, UploadFile
from main_web import pdf_processor
app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)


@app.post("/detect_plagiarism/upload_files/")
async def create_upload_file(
    source_file: UploadFile = File(..., description="source pdf file"), 
    target_file: UploadFile = File(..., description="target pdf file")
    ):

    response_data = {
        "status": False,
        "message": ""
    }
    
    if source_file.content_type not in ["application/pdf"]:
        response_data["message"] = "Invalid source file format."
        return response_data
    # save source file
    contents = await source_file.read()
    save_file(os.path.join(UPLOAD_FOLDER, source_file.filename), contents)
    
    if target_file.content_type not in ["application/pdf"]:
        response_data["message"] = "Invalid target file format."
        return response_data
    # save target file
    contents = await target_file.read()
    save_file(os.path.join(UPLOAD_FOLDER, target_file.filename), contents)
            
    origin_path = os.path.join(UPLOAD_FOLDER, source_file.filename)
    target_path = os.path.join(UPLOAD_FOLDER, target_file.filename)

    check_res = pdf_processor(origin_path, target_path, thresh=70)
    response_data["status"] = check_res["stats"]
    response_data["message"] = check_res["descript"]
    os.remove(origin_path)
    os.remove(target_path)

    return response_data