import os
import fitz


class PDFConverter:

    def __init__(self, dpi=300):

        self.dpi = dpi

        self.zoom = dpi / 72

        self.matrix = fitz.Matrix(
            self.zoom,
            self.zoom
        )

    def convert(self,
                pdf_path,
                output_folder="output/images"):

        os.makedirs(
            output_folder,
            exist_ok=True
        )

        pdf = fitz.open(pdf_path)

        image_paths = []

        pdf_name = os.path.splitext(
            os.path.basename(pdf_path)
        )[0]

        for page_number in range(len(pdf)):

            page = pdf.load_page(page_number)

            pix = page.get_pixmap(
                matrix=self.matrix
            )

            image_name = (
                f"{pdf_name}_"
                f"page_{page_number+1}.png"
            )

            image_path = os.path.join(
                output_folder,
                image_name
            )

            pix.save(image_path)

            image_paths.append(image_path)

        pdf.close()

        return image_paths


if __name__ == "__main__":

    converter = PDFConverter()

    images = converter.convert(
        "uploads/sample.pdf"
    )

    print(images)
