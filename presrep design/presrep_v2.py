# Import system modules
from roy_pdf_library import PDFGenerator, PDFDrawer, Colors, create_pdf
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
import sys
import os

# Add parent directory to path to import roy_pdf_library
# This must happen BEFORE importing roy_pdf_library
# sys.path.insert() tells Python where to look for modules
# os.path.join() creates the path to the parent directory (..)
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# Import reportlab modules

# Import roy's custom PDF library
# This import comes AFTER the path setup above

# Create PDF with A4 page size
# A4 = standard paper size (210mm x 297mm)
# pagesize=A4 tells the PDF generator to use A4 dimensions
pdf = create_pdf("presrep_output.pdf", pagesize=A4)

# Get the drawer object to draw on the PDF
drawer = pdf.get_drawer()

# Define page dimensions for A4
# mm = millimeter units (converts mm to points for PDF)
page_width = 210 * mm   # A4 width = 210 millimeters
page_height = 297 * mm  # A4 height = 297 millimeters

# Define Chinese title font object
# This creates reusable font settings for Chinese titles
# fontsize=30 makes the font 30 points large
# STSong-Light is the Chinese font (no bold variant available)
# color=Colors.BLACK makes the text black
chinese_title_font = {
    'font': 'STSong-Light',
    'font_size': 30,
    'color': Colors.BLACK
}

# Define English title font object
# This creates reusable font settings for English titles
# fontsize=25 makes the font 25 points large
# Helvetica is a standard English font
# color=Colors.DARK_BLUE makes the text blue
english_title_font = {
    'font': 'Helvetica',
    'font_size': 25,
    'color': Colors.DARK_BLUE
}

# Define text_font object for bottom text on pages
# This font is used for the organization and location text
# fontsize=17 (reduced from 20 by 3 points)
# STSong-Light for Chinese characters
# Black color
text_font = {
    'font': 'STSong-Light',
    'font_size': 17,
    'color': Colors.BLACK
}

# Initialize page number counter
# This counter starts at 0 and increments for each page
# Used for page numbering on pages 3+
page_counter = 0

# Create 16 pages with ruler overlay
# range(16) means: repeat 16 times, from 0 to 15
for page_number in range(16):
    print(f"Creating page {page_number + 1} of 16...")

    # ============================================================
    # PAGE {page_number + 1} START
    # ============================================================
    print(f"### Starting Page {page_number + 1} ###")

    # Draw ruler on this page
    # draw_ruler() creates a grid with measurements
    # This helps you see exact positions when placing content
    drawer.draw_ruler(page_width, page_height)

    # Upload company.jpg at 430,720 on pages 1 and 2 only
    # page_number == 0 means page 1, page_number == 1 means page 2
    if page_number == 0 or page_number == 1:
        # Same size as company.jpg on page 1 (120×40)
        drawer.upload_image(
            image="p1/company.jpg",
            x=430,
            y=720,
            width=120,
            height=40
        )

    # ============================================================
    # PAGE 1 - TITLE PAGE
    # ============================================================
    # Upload images only on page 1
    # page_number == 0 means this is the first page
    if page_number == 0:
        # Upload footer image at bottom of page (page 1 only)
        # x=0, y=0 means bottom left corner
        # width=page_width makes it span the full page width
        # height=125 sets the footer height to 125 points
        drawer.upload_image(
            image="p1/footer.png",
            x=0,
            y=0,
            width=page_width,
            height=125
        )
        # upload_image() places an image on the PDF
        # x=40 means 40 points from the left edge
        # y=740 means 740 points from the bottom edge (near the top of the page)
        # width=120 sets the image width to 120 points
        # height=40 sets the image height to 40 points
        drawer.upload_image(
            image="p1/company.jpg",
            x=40,
            y=740,
            width=120,
            height=40
        )

        # Upload titlepage image on page 1
        # x=150 means 150 points from the left edge
        # y=410 means 410 points from the bottom edge (middle-upper area)
        # Width and height reduced by 30% (to 70% of original)
        # Assuming original is approximately 300×200, 70% = 210×140
        drawer.upload_image(
            image="p1/titlepage.jpg",
            x=150,
            y=410,
            width=210,
            height=140
        )

        # Upload title image on page 1
        # x=130 means 130 points from the left edge
        # y=380 means 380 points from the bottom edge
        # Width and height reduced by 30% (to 70% of original)
        # Assuming original is approximately 350×50, 70% = 245×35
        drawer.upload_image(
            image="p1/title.png",
            x=130,
            y=380,
            width=245,
            height=35
        )

    # ============================================================
    # PAGE 2
    # ============================================================
    # Upload images only on page 2
    # page_number == 1 means this is the second page
    if page_number == 1:
        # Upload page2titletext on page 2
        # x=130 means 130 points from the left edge
        # y=580 means 580 points from the bottom edge (moved from 670)
        # width=330 sets the image width to 330 points
        # height=120 sets the image height to 120 points
        drawer.upload_image(
            image="p2/p2titletext.png",
            x=130,
            y=580,
            width=330,
            height=120
        )

        # Add centered text on page 2 (moved from page 1)
        # Get canvas object to calculate text width for centering
        canvas_obj = pdf.get_canvas()

        # Draw first centered text at y=120
        # Using text_font object parameters
        # Text: "测评单位（测评师）：中科宜和（北京）"
        text1 = "测评单位（测评师）：中科宜和（北京）"
        # Calculate text width to center it
        # stringWidth() measures how wide the text will be
        text_width1 = canvas_obj.stringWidth(
            text1, text_font['font'], text_font['font_size'])
        # Calculate centered x position: (page_width - text_width) / 2
        centered_x1 = (page_width - text_width1) / 2
        # Draw the centered text using text_font parameters
        drawer.draw_string(
            x=centered_x1,
            y=120,
            text=text1,
            font=text_font['font'],
            font_size=text_font['font_size'],
            color=text_font['color']
        )

        # Draw second centered text at y=95
        # Using text_font object parameters
        # Text: "测评地点：北京市 / 北京市 / 海淀区"
        text2 = "测评地点：北京市 / 北京市 / 海淀区"
        # Calculate text width to center it
        text_width2 = canvas_obj.stringWidth(
            text2, text_font['font'], text_font['font_size'])
        # Calculate centered x position
        centered_x2 = (page_width - text_width2) / 2
        # Draw the centered text using text_font parameters
        drawer.draw_string(
            x=centered_x2,
            y=95,
            text=text2,
            font=text_font['font'],
            font_size=text_font['font_size'],
            color=text_font['color']
        )

    # ============================================================
    # PAGE 3+ - CONTENT PAGES
    # ============================================================
    # Add page number and title text on pages 3 and beyond
    # page_number >= 2 means page 3 or later
    if page_number >= 2:
        # Draw left-aligned text with page number
        # Format: page_counter + 20pts space + "员工抗压力和岗位胜任力报告"
        # Position: x=50, y=25 (bottom left area)
        # Font size: 10, black, STSong-Light, left aligned
        page_text = f"{page_counter}                    员工抗压力和岗位胜任力报告"
        drawer.draw_string(
            x=50,
            y=25,
            text=page_text,
            font="STSong-Light",
            font_size=10,
            color=Colors.BLACK
        )
        # Increment page counter for next page
        page_counter += 1

    # show_page() adds a new page to the PDF
    # We call this after each page except the last one
    if page_number < 15:  # If not the last page (pages 0-14)
        pdf.show_page()

# Save the PDF file
# This writes all the pages to the file on your computer
pdf.save()
print("PDF created successfully with 16 pages, A4 size, and ruler overlay!")
