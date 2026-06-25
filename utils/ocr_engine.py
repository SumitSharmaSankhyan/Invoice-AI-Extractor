import os
import cv2
import pytesseract


class OCREngine:

    def __init__(self):

        # Uncomment and change this path only if needed.
        #
        # Example:
        #
        # pytesseract.pytesseract.tesseract_cmd = (
        #     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        # )

        self.config = r'--oem 3 --psm 6'

    # ----------------------------------------

    def preprocess(self, image_path):

        image = cv2.imread(image_path)

        if image is None:
            raise Exception(f"Cannot open image: {image_path}")

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.GaussianBlur(
            gray,
            (3,3),
            0
        )

        gray = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        return gray

    # ----------------------------------------

    def read_image(self, image_path):

        processed = self.preprocess(image_path)

        text = pytesseract.image_to_string(

            processed,

            lang="eng",

            config=self.config

        )

        return text

    # ----------------------------------------

    def read_images(self, image_list):

        full_text = ""

        for image in image_list:

            print(f"Reading : {image}")

            text = self.read_image(image)

            full_text += "\n"
            full_text += "="*80
            full_text += "\n"

            full_text += text

            full_text += "\n"

        return full_text

    # ----------------------------------------

    def save_text(
        self,
        text,
        output_file="output/ocr_result.txt"
    ):

        os.makedirs(
            os.path.dirname(output_file),
            exist_ok=True
        )

        with open(

            output_file,

            "w",

            encoding="utf-8"

        ) as f:

            f.write(text)

        return output_file
