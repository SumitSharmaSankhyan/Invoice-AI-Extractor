import os
import fitz  # PyMuPDF


def pdf_to_images(pdf_path, output_folder="output/images", dpi=300):
    """
    Convert every page of a PDF into PNG images.

    Parameters
    ----------
    pdf_path : str
        Full path of PDF.

    output_folder : str
        Folder where images will be saved.

    dpi : int
        Image quality (300 recommended for OCR)

    Returns
    -------
    list
        List of generated image paths.
    """

    os.makedirs(output_folder, exist_ok=True)

    pdf = fitz.open(pdf_path)

    image_paths = []

    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    for page_number in range(len(pdf)):

        page = pdf.load_page(page_number)

        pix = page.get_pixmap(matrix=matrix)

        image_name = f"{pdf_name}_page_{page_number + 1}.png"

        image_path = os.path.join(output_folder, image_name)

        pix.save(image_path)

        image_paths.append(image_path)

    pdf.close()

    return image_paths
