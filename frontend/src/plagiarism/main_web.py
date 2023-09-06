import json
import os
from werkzeug.utils import secure_filename
import argparse
from pathlib import Path
from pdf_ocr import convert_pdf_txt
from plagiarism_check import plag_check
from image_utils import pdf_image_check

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def pdf_processor(origin_file, target_file, thresh):
    """
    plagiarism detection
    :param arguments: two pdf files
    :return: response data
    """
    result_data = {
        "stats": False,
        "descript": "",
        "data": None
    }
    # check source-file existence
    if origin_file is None or not os.path.isfile(origin_file):
        result_data["descript"] = f"No exist such file: {origin_file}"
        return result_data
    # check source-file extension
    if not origin_file.lower().endswith(".pdf"):
        result_data["descript"] = f"This file is not pdf file, {origin_file}"
        return result_data

    # check target-file existence
    if target_file is None or not os.path.isfile(target_file):
        result_data["descript"] = f"No exist such file: {target_file}"
        return result_data
    # check target-file extension
    if not target_file.lower().endswith(".pdf"):
        result_data["descript"] = f"This file is not pdf file, {target_file}"
        return result_data

    # print("\n----------------------------------------")
    # print("Source pdf file: {}".format(origin_file))
    # print("Target pdf file: {}".format(target_file))

    origin_path = Path(origin_file)
    target_path = Path(target_file)
    # output_file = 'results.json'
    output_file = "results.json"
    output_data = {}
    print("\n----------------------------------------")
    print("Start converting pdf to text ...")
    ocr_result = convert_pdf_txt(origin_path, target_path)
    if ocr_result["status"]:
        print("Conversion finished. Now detecting plagiarism ...")
        result = plag_check(ocr_result["paths"], thresh)

        message = f"Found the plagiarism content,\n" \
                  f"\t{round(result['source_percent'] * 100)}% matched with source file,\n" \
                  f"\t{round(result['target_percent'] * 100)}% matched with target file.\n" \
                  f"Result saved in {output_file}"
        print("\n----------------------------------------")
        print(message)
        result_data["stats"] = True
        result_data["descript"] = "Successfully processed.\nYou can find the result file in {}.".format(output_file)
        output_data["text_match"] = result
        # return result_data
    else:
        result_data["descript"] = ocr_result["descript"]
    print("Start image-comparison of pdfs")
    figure_checker = pdf_image_check(origin_path, target_path)
    images_match = figure_checker.run_image_check()
    output_data["image_match"] = images_match
    result_data["data"] = output_data
    print("\n----------------------------------------")
    print("Writing the result to file: {}".format(output_file))
    with open(output_file, "w") as result_file:
        result_file.write(json.dumps(result_data["data"], indent=4))

    return result_data
