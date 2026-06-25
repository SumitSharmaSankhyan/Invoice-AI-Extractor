import os
import cv2
import pytesseract


# ----------------------------------------------------
# IMPORTANT
# ----------------------------------------------------
# Uncomment and edit this ONLY if Tesseract is not
# in your system PATH.
#
# Windows Example:
#
# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# )
#
# ----------------------------------------------------


def preprocess_image(image_path):
    """
    Improve image quality before OCR.
    """

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    gray = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return gray


def extract_text(image_path):
    """
    OCR from a single image.
    """

    processed = preprocess_image(image_path)

    custom_config = r'--oem 3 --psm 6'

    text = pytesseract.image_to_string(
        processed,
        lang="eng",
        config=custom_config
    )

    return text


def extract_from_images(image_paths):
    """
    OCR from multiple images.
    """

    complete_text = ""

    for image in image_paths:

        print("Reading:", image)

        page_text = extract_text(image)

        complete_text += "\n"
        complete_text += "=" * 70
        complete_text += "\n"

        complete_text += page_text

        complete_text += "\n"

    return complete_text


def save_text(text, filename="output/ocr_result.txt"):

    folder = os.path.dirname(filename)

    os.makedirs(folder, exist_ok=True)

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(text)

    return filename
