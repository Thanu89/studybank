import shutil
import os
from pikepdf import Pdf, PdfImage
from skimage.metrics import structural_similarity
import cv2


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class pdf_image_check(object):
    def __init__(self, pdf_1_path="", pdf_2_path="", threshold=0.9):
        self.minimum_commutative_image_diff = 1
        self.pdf_1_path = pdf_1_path
        self.pdf_2_path = pdf_2_path
        self.threshold = threshold
        self.first_folder = os.path.join(UPLOAD_FOLDER, "first")
        self.second_folder = os.path.join(UPLOAD_FOLDER, "second")
        self.initialize()

    def initialize(self):
        if os.path.exists(self.first_folder):
            shutil.rmtree(self.first_folder, ignore_errors=False, onerror=None)
        os.makedirs(self.first_folder)
        if os.path.exists(self.second_folder):
            shutil.rmtree(self.second_folder, ignore_errors=False, onerror=None)
        os.makedirs(self.second_folder)
    
    #Returns the matched images from the 2 PDFs
    def run_image_check(self):
        if not os.path.exists(self.pdf_1_path):
            print(f"No exist pdf file: {self.pdf_1_path}")
            return []
        if not os.path.exists(self.pdf_2_path):
            print(f"No exist pdf file: {self.pdf_2_path}")
            return []
        print(f"\tExtracting images from {self.pdf_1_path}")
        first_images = extract_image(self.pdf_1_path, self.first_folder)
        print(f"\tExtracting images from {self.pdf_2_path}")
        second_images = extract_image(self.pdf_2_path, self.second_folder)
        matched_images = []
        for target_img in second_images:
            scores = []
            for src_img in first_images:
                similarity_score = compare_images(src_img, target_img)
                scores.append(similarity_score)
            if max(scores) < self.threshold:
                continue
            else:
                max_index = scores.index(max(scores))
                matched_images.append([first_images[max_index], target_img, max(scores)])
        return matched_images


def extract_image(pdf_file, save_folder):

    image_paths = []
    if not os.path.exists(pdf_file):
        print("No exists such file.")
        return image_paths
    example = Pdf.open(pdf_file)
    basename = os.path.basename(pdf_file)
    for i, page in enumerate(example.pages):
        for j, (name, raw_image) in enumerate(page.images.items()):
            image = PdfImage(raw_image)
            image_path = f"./{save_folder}/{basename}-page{i:03}-img{j:03}"
            out = image.extract_to(fileprefix=image_path)
    image_names = [img for img in os.listdir(save_folder)]
    image_paths = [os.path.join(save_folder, img) for img in image_names]
    return image_paths


def compare_images(first_image, second_image):

    if not os.path.exists(first_image):
        print(f"No exists such file: {first_image}")
        return -1
    if not os.path.exists(second_image):
        print(f"No exists such file: {second_image}")
        return -1
    # read images with opencv
    first = cv2.imread(first_image)
    second = cv2.imread(second_image)

    # consistent the size of images
    if first.shape != second.shape:
        width = int(first.shape[1])
        height = int(first.shape[0])
        second = cv2.resize(second, (width, height))

    # Convert images to grayscale
    first_gray = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
    second_gray = cv2.cvtColor(second, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    score, diff = structural_similarity(first_gray, second_gray, full=True)
    return score
