import json
import os
from flask import make_response, request, send_file
from flask_restful import Resource
import base64
from main_web import pdf_processor, UPLOAD_FOLDER


def get_result():
    output_file = 'uploads/plagiarism.json'
    link = send_file(output_file, attachment_filename=os.path.basename(output_file),
                     as_attachment=True)
    return link


def file_save(base64_data, filepath):
    """
    receive and process file data in base64 type
    """
    if os.path.exists(filepath):
        os.remove(filepath)
    try:
        encoded_data = base64_data.split(',')[-1]
        dict_buf = base64.b64decode(encoded_data)
        with open(filepath, 'wb') as f:
            f.write(dict_buf)
        return True, f"Successfully Saved: {filepath}"
    except Exception as error:
        print(repr(error))
        return False, "Failed to receive uploading file."


class Main_Class(Resource):
    def __init__(self):
        self.response_data = {
            'status': 'fail',
            'message': ['invalid payload']
        }
        # self._db_ = load_model()

    def post(self):
        is_parse = request.is_json
        if not is_parse:
            self.response_data["message"] = ['Failed to receive data.']
            response = json.dumps(self.response_data, indent=2)
            return make_response(response, 200)

        content = request.get_json()
        try:
            command = content['command']
        except Exception as error:
            self.response_data["message"] = [repr(error)]
            response = json.dumps(self.response_data, indent=2)
            return make_response(response, 200)

        if command == 'plagiarism_check':
            _data_ = content['message']
            source_data = _data_["first_file_data"]
            source_name = _data_["first_file_name"]
            target_data = _data_["second_file_data"]
            target_name = _data_["second_file_name"]
            limit = int(_data_["limit"])
            source_path = os.path.join(UPLOAD_FOLDER, "source_" + source_name)
            target_path = os.path.join(UPLOAD_FOLDER, "target_" + target_name)
            src_success, _ = file_save(source_data, source_path)
            target_success, _ = file_save(target_data, target_path)
            if src_success and target_success:
                check_res = pdf_processor(source_path, target_path, limit)
                res_data = [check_res]
                os.remove(source_path)
                os.remove(target_path)
            else:
                res_data = ["Failed to upload files"]
            self.response_data["status"] = "success"
        else:
            res_data = ["Invalid operation."]

        self.response_data["message"] = res_data
        response = json.dumps(self.response_data, indent=2)
        return make_response(response, 200)
