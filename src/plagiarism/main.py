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


def main(arguments):
    """
    plagiarism detection
    :param arguments: two pdf files
    :return: response data
    """

    origin_file = arguments.source
    target_file = arguments.target
    thresh = arguments.limit

    # check source-file existence
    if origin_file is None or not os.path.isfile(origin_file):
        print(f"No exist such file: {origin_file}")
        return
    # check source-file extension
    if not origin_file.lower().endswith(".pdf"):
        print(f"This file is not pdf file, {origin_file}")
        return
    
    # check target-file existence
    if target_file is None or not os.path.isfile(target_file):
        print(f"No exist such file: {target_file}")
        return 
    # check target-file extension
    if not target_file.lower().endswith(".pdf"):
        print(f"This file is not pdf file, {target_file}")
        return 

    print("\n----------------------------------------")
    print("Source pdf file: {}".format(origin_file))
    print("Target pdf file: {}".format(target_file))

    origin_path = Path(origin_file)
    target_path = Path(target_file)
    output_file = os.path.join(
        UPLOAD_FOLDER,
        secure_filename(origin_file) + "_" + secure_filename(target_file) + ".json"
        )
    
    output_data = {}
    
    print("\n----------------------------------------")
    print("Start converting pdf to text ...")
    ocr_result = convert_pdf_txt(origin_path, target_path)
    if ocr_result["status"]:
        print("Conversion finished. Now detecting plagiarism ...")
        result = plag_check(ocr_result["paths"], thresh)
        output_data["text_match"] = result


        message = f"Found the plagiarism content,\n" \
                  f"\t{round(result['source_percent'] * 100)}% matched with source file,\n" \
                  f"\t{round(result['target_percent'] * 100)}% matched with target file.\n" \
                  f"Result saved in {output_file}"
        print("\n----------------------------------------")
        print(message)
    else:
        print(ocr_result["descript"])

    print("Start image-comparison of pdfs")
    figure_checker = pdf_image_check(origin_path, target_path)
    images_match = figure_checker.run_image_check()
    output_data["image_match"] = images_match

    print("\n----------------------------------------")
    print("Writing the result to file: {}".format(output_file))
    with open(output_file, "w") as result_file:
        result_file.write(json.dumps(output_data, indent=4))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--source", type=str, required=True, default="one.pdf",
                        help="path of origin pdf file ")
    parser.add_argument("-t", "--target", type=str, required=True, default="two.pdf",
                        help="path of pdf file to be compared")
    parser.add_argument("-l", "--limit", type=int, default=70,
                        help="limit value of similarity between two strings(sentences)")
    args = parser.parse_args()
    main(args)
