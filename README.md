# 💫 About This Project:
My Final Year Project. A website that allows users to upload their notes so they can then sell the notes to other users. To ensure there is no copyright enfringement the website will then directly compare the notes to the original source of where the notes are derived from, usually a textbook in order to check for plagiarism. Plagiarism detection is done on both text and images before allowing the user to sell their notes on the website.<br>


# 💻 Tech Stack:
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![Java](https://img.shields.io/badge/java-%23ED8B00.svg?style=for-the-badge&logo=openjdk&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) ![React Query](https://img.shields.io/badge/-React%20Query-FF4154?style=for-the-badge&logo=react%20query&logoColor=white) ![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white) ![Express.js](https://img.shields.io/badge/express.js-%23404d59.svg?style=for-the-badge&logo=express&logoColor=%2361DAFB) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

## Prerequisites

### Tesseract Installation

1. On Ubuntu, you can install tesseract using the command below.

```
sudo apt update
sudo apt install tesseract-ocr
```

2. On Windows, go to [GitHub](https://github.com/UB-Mannheim/tesseract/wiki), download the tesseract installer, install it and add Tesseract installation folder to the PATH environment variable.

![Tesseract install example](tesseract_set.png)

And make sure that you change the path of the real installation in the head of pdf_ocr.py file as shown below.

```
if 'win32' in sys.platform:
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
```

And you should also install the poppler library. Please download **_poppler_** for pdf2image. Please refer to this [GitHub](https://github.com/Belval/pdf2image).

### Opencv Installation

1. On Ubuntu, you can install opencv using the command below.

```commandline
sudo apt update
sudo apt install libopencv-dev python3-opencv
```

2. On Windows, download opencv-installer(version=4.1.0) and install opencv using it. Please refer to this [here](https://learnopencv.com/install-opencv-on-windows/)

## Install Dependencies

Install the libraries using the below commands.

```
pip3 install -r requirements.txt
```

## How it works

This algorithm consists of two main steps.
First is _OCR_ step that converts the given pdf files to text files using _tesseract-ocr_.
Second is plagiarism step that compares the text files using fuzzywuzzy.

## How to use

### Using command-line

You can run the below command to get the results.
Here, the parameter _source_ points the source file for the comparison, which is the notes.
Parameter _target_ points the target file, which is the textbook.
Parameter _limit_ (optional) is an integer between 0 and 100 which is a threshold value of similarity between two strings(sentences). Default value is 70.

```
python3 main.py -s source_file.pdf -t target_file.pdf -l 70

usage:
    -s, --source: path of origin pdf file
    -t, --target: path of pdf file to be compared
    -l, --limit: limit value of similarity between two strings(sentences), default is 70
```

Here are the sample test results. Results are saved in **_"results.json"_**

```
python main.py -s one.pdf -t two.pdf

----------------------------------------
Source pdf file: one.pdf
Target pdf file: two.pdf

----------------------------------------
Start converting pdf to text ...
        Converting PDF to IMAGE: one.pdf
        OCR processing ...
        Converting PDF to IMAGE: two.pdf
        OCR processing ...
Conversion finished. Now detecting plagiarism ...

----------------------------------------
Comparing two files...

----------------------------------------
Writing the result to file: uploads\one.pdf_two.pdf.json

----------------------------------------
Found the plagiarism content,
        0% matched with source file,
        0% matched with target file.
Result saved in uploads\one.pdf_two.pdf.json
```

### Using API

You need to run the API service before running this.
`uvicorn api_service:app`

### Using Web Browser

First start the servers for the frontend and the backend by going to the respective directories and running the command `npm start`
Afterwards start the API using the above command and then go to http://localhost:3000/. Then create an account/log in and then go to the
drop down menu and navigate to the plagiarism checker page. Now upload two PDF files and wait for the algorithm to return the JSON file.

### Studybank
My Final Year Project. A website that allows users to upload their notes so they can then sell the notes to other users. To ensure there is no copyright enfringement the website will then directly compare the notes to the original source of where the notes are derived from, usually a textbook in order to check for plagiarism. Plagiarism detection is done on both text and images before allowing the user to sell their notes on the website.


