from datetime import datetime

import uuid
import validators
import urllib.request
import urllib.parse
import pytesseract
import cv2
import numpy as np
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

app = FastAPI()


@app.get('/ping')
async def ping():
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')


class PDFToTextBody(BaseModel):
    pdf_path: str

    class Config:
        schema_extra = {
            "pdf_path": "http://www.africau.edu/images/default/sample.pdf"
        }


@app.post('/pdf-to-text/ko')
async def pdfToText(
    body: PDFToTextBody = Body(example={
                               "pdf_path": "http://www.africau.edu/images/default/sample.pdf"}, description="pdf to text api")):
    try:
        # Url including Korean is allowed
        pdf_path = body.pdf_path

        if pdf_path is None or pdf_path == '':
            raise HTTPException(status_code=400, detail="MISSING_QUERY")

        if validators.url(pdf_path) is not True:
            raise HTTPException(status_code=400, detail="PDF_PATH_IS_NOT_URL")

        url_info = urllib.parse.urlsplit(pdf_path)
        encoding_url = f'{url_info.scheme}://{url_info.netloc}{urllib.parse.quote(url_info.path)}'

        req = urllib.request.urlopen(encoding_url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)

        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        random_uuid = uuid.uuid4()
        image_path = f'images/{random_uuid}.jpg'

        cv2.imwrite(image_path, gray_image,
                    [int(cv2.IMWRITE_JPEG_QUALITY), 100])

        image = cv2.imread(image_path)

        #     --psm NUM             Specify page segmentation mode.
        #     --oem NUM             Specify OCR Engine mode.
        #     Page segmentation modes:
        #   0    Orientation and script detection (OSD) only.
        #   1    Automatic page segmentation with OSD.
        #   2    Automatic page segmentation, but no OSD, or OCR.
        #   3    Fully automatic page segmentation, but no OSD. (Default)
        #   4    Assume a single column of text of variable sizes.
        #   5    Assume a single uniform block of vertically aligned text.
        #   6    Assume a single uniform block of text.
        #   7    Treat the image as a single text line.
        #   8    Treat the image as a single word.
        #   9    Treat the image as a single word in a circle.
        #  10    Treat the image as a single character.
        #  11    Sparse text. Find as much text as possible in no particular order.
        #  12    Sparse text with OSD.
        #  13    Raw line. Treat the image as a single text line,
        #        bypassing hacks that are Tesseract-specific.

        # OCR Engine modes: (see https://github.com/tesseract-ocr/tesseract/wiki#linux)
        #   0    Legacy engine only.
        #   1    Neural nets LSTM engine only.
        #   2    Legacy + LSTM engines.
        #   3    Default, based on what is available.

        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(
            image, lang="kor+eng", config=custom_config)

        return text
    except Exception as error:
        HTTPException(status_code=500, detail=error)
