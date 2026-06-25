from utils.pdf_converter import pdf_to_images

images = pdf_to_images(
    "uploads/N2-11269-4.pdf"
)

print(images)
