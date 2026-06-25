import os
import fitz


class PDFConverter:
    """
    Convert PDF pages into high-resolution PNG images.
    """

    def __init__(self, dpi=300):
        self.dpi = dpi
        self.zoom = dpi / 72
        self.matrix = fitz.Matrix(self.zoom, self.zoom)

    # -----------------------------------------

    def convert(self, pdf_path, output_root="output/images"):

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        pdf_name = os.path.splitext(
            os.path.basename(pdf_path)
        )[0]

        output_folder = os.path.join(
            output_root,
            pdf_name
        )

        os.makedirs(output_folder, exist_ok=True)

        image_paths = []

        document = fitz.open(pdf_path)

        try:

            for page_number in range(len(document)):

                page = document.load_page(page_number)

                pix = page.get_pixmap(
                    matrix=self.matrix,
                    alpha=False
                )

                image_path = os.path.join(
                    output_folder,
                    f"page_{page_number + 1}.png"
                )

                pix.save(image_path)

                image_paths.append(image_path)

        finally:

            document.close()

        return image_paths

    # -----------------------------------------

    def convert_multiple(
        self,
        pdf_files,
        output_root="output/images"
    ):

        all_images = {}

        for pdf in pdf_files:

            all_images[pdf] = self.convert(
                pdf,
                output_root
            )

        return all_images

    # -----------------------------------------

    def count_pages(self, pdf_path):

        document = fitz.open(pdf_path)

        pages = len(document)

        document.close()

        return pages

    # -----------------------------------------

    def pdf_info(self, pdf_path):

        document = fitz.open(pdf_path)

        info = {

            "file": os.path.basename(pdf_path),

            "pages": len(document),

            "metadata": document.metadata

        }

        document.close()

        return info


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    converter = PDFConverter()

    sample_pdf = "uploads/sample.pdf"

    if os.path.exists(sample_pdf):

        print("PDF Information")

        print(converter.pdf_info(sample_pdf))

        images = converter.convert(sample_pdf)

        print()

        print("Generated Images")

        for img in images:
            print(img)

    else:

        print("Place a sample.pdf inside uploads folder.")
