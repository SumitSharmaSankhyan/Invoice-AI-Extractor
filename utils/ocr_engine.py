import os
import cv2
import pytesseract


class OCREngine:
    """
    OCR Engine using Tesseract
    """

    def __init__(self):

        # Uncomment and change ONLY if needed.
        #
        # Example:
        #
        # pytesseract.pytesseract.tesseract_cmd = \
        # r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        self.config = r'--oem 3 --psm 6'

    # --------------------------------------------------

    def preprocess(self, image_path):

        image = cv2.imread(image_path)

        if image is None:
            raise Exception(
                f"Unable to open image : {image_path}"
            )

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

    # --------------------------------------------------

    def image_to_text(self, image_path):

        processed = self.preprocess(image_path)

        text = pytesseract.image_to_string(

            processed,

            lang="eng",

            config=self.config

        )

        return text

    # --------------------------------------------------

    def images_to_text(self, image_list):

        full_text = ""

        for image in image_list:

            print(f"Reading OCR : {image}")

            page_text = self.image_to_text(image)

            full_text += "\n"
            full_text += "=" * 80
            full_text += "\n"

            full_text += page_text

            full_text += "\n"

        return full_text

    # --------------------------------------------------

    def save_text(
        self,
        text,
        filename="output/ocr_result.txt"
    ):

        folder = os.path.dirname(filename)

        os.makedirs(
            folder,
            exist_ok=True
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(text)

        return filename

    # --------------------------------------------------

    def extract(self, image_list):

        text = self.images_to_text(image_list)

        self.save_text(text)

        return text


# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    from pdf_converter import PDFConverter

    converter = PDFConverter()

    images = converter.convert(
        "uploads/sample.pdf"
    )

    ocr = OCREngine()

    text = ocr.extract(images)

    print(text)
