from PyPDF2 import PdfReader
from pdf2image import convert_from_path

# Load the PDF to extract images
pdf_path = "CF-Advanced-Infantry.pdf"

# Extract images from each page of the PDF
images = convert_from_path(pdf_path)

# Save the extracted images
image_paths = []
for i, image in enumerate(images):
    image_path = f"advanced_infantry_image_{i + 1}.jpg"
    image.save(image_path, "JPEG")
    image_paths.append(image_path)

image_paths
