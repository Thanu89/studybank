import os
import sys
import random
import pdf2image
import pytesseract
from pytesseract import Output

if 'win32' in sys.platform:
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

UPLOADS = "uploads"
os.makedirs(UPLOADS, exist_ok=True)


def ocr_pdf2txt(pdf_path):
    """
    convert pdf to text file
    :param pdf_path: pdf file path
    :return: path of converted text file
    """
    txt_name = "{}.txt".format(str(random.randint(0, 0x7fffffffffffffff)))
    txt_path = os.path.join(UPLOADS, txt_name)
    if os.path.exists(txt_path):
        os.remove(txt_path)
    
    print("\tConverting PDF to IMAGE: {}".format(pdf_path))
    try:
        images = pdf2image.convert_from_path(pdf_path)
    except Exception as error:
        print(repr(error))
        raise("pdf2image error")

    print("\tOCR processing ...")
    page_num = 1
    with open(txt_path, "w") as txt_file:
        for pil_im in images:
            ocr_dict = pytesseract.image_to_data(pil_im, lang='eng', output_type=Output.DICT)
            # ocr_dict now holds all the OCR info including text and location on the image
            try:
                text = ocr_dict_txt(ocr_dict)
            except Exception as error:
                print(repr(error))
                continue
            page_num += 1
            txt_file.write("{}\n".format(text))

    return txt_path


def ocr_dict_txt(ocr_dict: dict):
    """
    get text from ocr result dict
    :param ocr_dict: dict resulted from ocr
    :return: string
    """
    block_num = ocr_dict['block_num']
    par_num = ocr_dict['par_num']

    text = ocr_dict["text"]
    words_num = ocr_dict["word_num"]
    confidences = ocr_dict["conf"]
    # print("confidence: {}".format(confidences))
    length = len(confidences)
    page_content = []
    para_content = []
    prev_block_index = block_num[0]
    prev_para_index = par_num[0]
    for index in range(length):
        block_id = block_num[index]
        para_id = par_num[index]
        if block_id == prev_block_index and para_id == prev_para_index:
            if words_num[index] == 0:
                continue
            # print("INFO: {}".format(confidences[index]))
            if float(confidences[index]) < 50:
                continue
            para_content.append(text[index])
        else:
            new_para_text = " ".join(para_content)
            if new_para_text.strip() != "":
                page_content.append(new_para_text.strip())
            para_content = []
            prev_block_index = block_id
            prev_para_index = para_id
        if index == len(block_num) - 1:
            last_para_text = " ".join(para_content)
            if last_para_text.strip() != "":
                page_content.append(last_para_text.strip())

    return "\n".join(page_content)


def convert_pdf_txt(origin, target):
    res_data = {
        "status": False,
        "descript": "",
        "paths": []
    }

    try:
        origin_txt_path = ocr_pdf2txt(origin)
    except Exception as error:
        res_data["descript"] = f"Failed to ocr {origin}: {repr(error)}"
        return res_data

    try:
        target_txt_path = ocr_pdf2txt(target)
    except Exception as error:
        res_data["descript"] = f"Failed to ocr {target}: {repr(error)}"
        return res_data

    res_data["status"] = True
    res_data["descript"] = "Success to ocr"
    res_data["paths"] = [origin_txt_path, target_txt_path]
    return res_data
