# Import system modules
import sys
import os

# Change to the script's directory to ensure relative paths work
# This makes sure image files can be found regardless of where the script is run from
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Add parent directory to path to import roy_pdf_library
# This must happen BEFORE importing roy_pdf_library
# sys.path.insert() tells Python where to look for modules
# os.path.join() creates the path to the parent directory (..)
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# Import roy's custom PDF library
# This import comes AFTER the path setup above
from roy_pdf_library import PDFGenerator, PDFDrawer, Colors, create_pdf

# Import reportlab modules
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas

# Create PDF with A4 page size
# A4 = standard paper size (210mm x 297mm)
# pagesize=A4 tells the PDF generator to use A4 dimensions
pdf = create_pdf("presrep_output_v3.pdf", pagesize=A4)

# Get the drawer object to draw on the PDF
drawer = pdf.get_drawer()

# Define page dimensions for A4
# mm = millimeter units (converts mm to points for PDF)
page_width = 210 * mm   # A4 width = 210 millimeters
page_height = 297 * mm  # A4 height = 297 millimeters

# Define function to upload full-page image
def upload_page_image(drawer, image_name, page_num, target_page):
    """
    Upload a full-page image if current page matches target page
    Parameters:
        drawer: PDFDrawer object
        image_name: Name of the image file (e.g., "0.png")
        page_num: Current page number (0-indexed)
        target_page: Target page number to display image (0-indexed)
    """
    if page_num == target_page:
        drawer.upload_image(
            image=f"original_png/{image_name}",
            x=0,
            y=0,
            width=page_width,
            height=page_height
        )

# Initialize page number counter
page_counter = 1

# Create 16 pages with ruler overlay
# range(16) means: repeat 16 times, from 0 to 15
for page_number in range(16):
    print(f"Creating page {page_number + 1} of 16...")

    # ============================================================
    # PAGE {page_number + 1} START
    # ============================================================
    print(f"### Starting Page {page_number + 1} ###")

    # Upload full-page images FIRST (so they appear under the ruler)
    upload_page_image(drawer, "0.png", page_number, 0)
    upload_page_image(drawer, "02.png", page_number, 1)
    upload_page_image(drawer, "03.png", page_number, 2)
    upload_page_image(drawer, "04.png", page_number, 3)
    upload_page_image(drawer, "05.png", page_number, 4)
    upload_page_image(drawer, "06.png", page_number, 5)
    upload_page_image(drawer, "07.png", page_number, 6)
    upload_page_image(drawer, "08.png", page_number, 7)
    upload_page_image(drawer, "09.png", page_number, 8)
    upload_page_image(drawer, "010.png", page_number, 9)
    upload_page_image(drawer, "011.png", page_number, 10)
    upload_page_image(drawer, "012.png", page_number, 11)
    upload_page_image(drawer, "013.png", page_number, 12)
    upload_page_image(drawer, "014.png", page_number, 13)
    upload_page_image(drawer, "015.png", page_number, 14)
    upload_page_image(drawer, "016.png", page_number, 15)

    # Draw ruler on TOP of the images
    # draw_ruler() creates a grid with measurements
    # This helps you see exact positions when placing content
    drawer.draw_ruler(page_width, page_height)

    # show_page() adds a new page to the PDF
    # We call this after each page except the last one
    if page_number < 15:  # If not the last page (pages 0-14)
        pdf.show_page()

# Save the PDF file
# This writes all the pages to the file on your computer
pdf.save()
print("PDF created successfully with 16 pages, A4 size, and ruler overlay!")

