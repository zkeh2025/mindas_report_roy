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
pdf = create_pdf("presrep_output.pdf", pagesize=A4)

# Get the drawer object to draw on the PDF
drawer = pdf.get_drawer()

# Define page dimensions for A4
# mm = millimeter units (converts mm to points for PDF)
page_width = 210 * mm   # A4 width = 210 millimeters
page_height = 297 * mm  # A4 height = 297 millimeters

# Define Chinese title font object
# This creates reusable font settings for Chinese titles
# fontsize=27 makes the font 27 points large (reduced by 3 pts)
# STSong-Light is the Chinese font (no bold variant available)
# color=Colors.BLACK makes the text black
chinese_title_font = {
    'font': 'STSong-Light',
    'font_size': 27,
    'color': Colors.BLACK
}

# Define English title font object
# This creates reusable font settings for English titles
# fontsize=20, Helvetica font, Blue color
english_title_font = {
    'font': 'Helvetica',
    'font_size': 20,
    'color': [0, 0, 1]  # Blue color in RGB
}

# Define Chinese subtitle font object
# Black color, font size 15, STSong-Light
chinese_subtitle_font = {
    'font': 'STSong-Light',
    'font_size': 15,
    'color': Colors.BLACK  # Black color
}

# Define English subtitle font object
# Black color, font size 15, Helvetica
english_subtitle_font = {
    'font': 'Helvetica',
    'font_size': 15,
    'color': Colors.BLACK  # Black color
}

# Define text_font object for paragraph text
# Light grey color, font size 12, STSong-Light
text_font = {
    'font': 'STSong-Light',
    'font_size': 12,
    'color': [0.7, 0.7, 0.7]  # Light grey color
}

# Define page2_text_font object for page 2 bottom text
# Black color, font size 17, STSong-Light
page2_text_font = {
    'font': 'STSong-Light',
    'font_size': 17,
    'color': Colors.BLACK
}

# Define big_title_font object for page 1 title text
# This font is used for the main title text on page 1
# fontsize=30, STSong-Light for Chinese characters, Blue color
big_title_font = {
    'font': 'STSong-Light',
    'font_size': 30,
    'color': Colors.DARK_BLUE
}

# Define paragraph_title function to draw Chinese + separator + English subtitle
def draw_paragraph_title(drawer, canvas_obj, x, y, chinese_text, english_text):
    """
    Draw a paragraph title with Chinese text, vertical line separator, and English text
    Dynamically calculates spacing based on Chinese text width
    Parameters:
        drawer: PDFDrawer object
        canvas_obj: Canvas object for calculating text width
        x: x position for Chinese text start
        y: y position for baseline
        chinese_text: Chinese subtitle text
        english_text: English subtitle text
    """
    # Draw Chinese subtitle
    drawer.draw_string(
        x=x,
        y=y,
        text=chinese_text,
        font=chinese_subtitle_font['font'],
        font_size=chinese_subtitle_font['font_size'],
        color=chinese_subtitle_font['color']
    )
    
    # Calculate Chinese text width
    chinese_width = canvas_obj.stringWidth(
        chinese_text,
        chinese_subtitle_font['font'],
        chinese_subtitle_font['font_size']
    )
    
    # Calculate position for vertical line (chinese_width + 20 points)
    line_x = x + chinese_width + 20
    
    # Draw vertical line separator
    drawer.draw_line(
        x1=line_x,
        y1=y + 15,
        x2=line_x,
        y2=y,
        width=1,
        color=Colors.BLACK  # Black color to match subtitles
    )
    
    # Draw English subtitle (20 points after line)
    drawer.draw_string(
        x=line_x + 20,
        y=y,
        text=english_text,
        font=english_subtitle_font['font'],
        font_size=english_subtitle_font['font_size'],
        color=english_subtitle_font['color']
    )

# Define function to draw Chinese title
def draw_chinese_title(drawer, x, y, text, font_size=None):
    """
    Draw Chinese title text
    Parameters:
        drawer: PDFDrawer object
        x: x position
        y: y position
        text: Chinese title text
        font_size: Optional font size (defaults to chinese_title_font size)
    """
    size = font_size if font_size is not None else chinese_title_font['font_size']
    drawer.draw_string(
        x=x,
        y=y,
        text=text,
        font=chinese_title_font['font'],
        font_size=size,
        color=chinese_title_font['color']
    )

# Define function to draw English title
def draw_english_title(drawer, x, y, text, font_size=None, font=None):
    """
    Draw English title text
    Parameters:
        drawer: PDFDrawer object
        x: x position
        y: y position
        text: English title text
        font_size: Optional font size (defaults to english_title_font size)
        font: Optional font (defaults to english_title_font font)
    """
    size = font_size if font_size is not None else english_title_font['font_size']
    font_name = font if font is not None else english_title_font['font']
    drawer.draw_string(
        x=x,
        y=y,
        text=text,
        font=font_name,
        font_size=size,
        color=english_title_font['color']
    )

# Define function to draw justified paragraph
def draw_paragraph(canvas_obj, x, y, width, height, text):
    """
    Draw justified paragraph with specified dimensions
    Parameters:
        canvas_obj: Canvas object for drawing
        x: x position
        y: y position (top of paragraph)
        width: paragraph width
        height: paragraph height
        text: paragraph text
    """
    # Register Chinese font for reportlab
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    
    # Create paragraph style
    para_style = ParagraphStyle(
        'JustifiedParagraph',
        fontName='STSong-Light',
        fontSize=text_font['font_size'],
        textColor=colors.Color(text_font['color'][0], text_font['color'][1], text_font['color'][2]),
        alignment=TA_JUSTIFY,
        leading=text_font['font_size'] * 1.2
    )
    
    # Create and draw paragraph
    para = Paragraph(text, para_style)
    para.wrapOn(canvas_obj, width, height)
    para.drawOn(canvas_obj, x, y - height)  # Subtract height for top-to-bottom positioning

# Initialize page number counter
# This counter starts at 1 so page 3 displays "1"
# Used for page numbering on pages 3+
page_counter = 1

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

    # Upload header image on pages 2-16 at y=800
    # page_number >= 1 means page 2 and beyond
    if page_number >= 1:
        drawer.upload_image(
            image="p3/header.png",
            x=0,
            y=800,
            width=page_width,
            height=40
        )
    
    # Upload company logo on pages 3-16 at bottom right
    # page_number >= 2 means page 3 and beyond
    if page_number >= 2:
        drawer.upload_image(
            image="p1/company.jpg",
            x=490,
            y=20,
            width=50,
            height=20
        )

    # Upload footer image only on page 2
    # x=0, y=0 means bottom left corner
    # width=page_width makes it span the full page width
    if page_number == 1:
        drawer.upload_image(
            image="p2/footer.png",
            x=0,
            y=0,
            width=page_width,
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
        # x=35 (decreased by 75 from 110)
        # y=410 means 410 points from the bottom edge (middle-upper area)
        # width=530 (increased by 150 from 380), height=290 (700-410)
        drawer.upload_image(
            image="p1/titlepage.jpg",
            x=35,
            y=410,
            width=530,
            height=290
        )

        # Draw centered text "员工抗压力" on page 1
        # Get canvas object to calculate text width for centering
        canvas_obj = pdf.get_canvas()
        text_page1 = "员工抗压力"
        # Calculate text width to center it using big_title_font parameters
        text_width_page1 = canvas_obj.stringWidth(
            text_page1, big_title_font['font'], big_title_font['font_size'])
        # Calculate centered x position: (page_width - text_width) / 2
        centered_x_page1 = (page_width - text_width_page1) / 2
        # Draw the centered text using big_title_font parameters
        drawer.draw_string(
            x=centered_x_page1,
            y=340,
            text=text_page1,
            font=big_title_font['font'],
            font_size=big_title_font['font_size'],
            color=big_title_font['color']
        )

        # Draw centered text "和岗位胜任力报告" on page 1
        text_page1_line2 = "和岗位胜任力报告"
        # Calculate text width to center it using big_title_font parameters
        text_width_page1_line2 = canvas_obj.stringWidth(
            text_page1_line2, big_title_font['font'], big_title_font['font_size'])
        # Calculate centered x position
        centered_x_page1_line2 = (page_width - text_width_page1_line2) / 2
        # Draw the centered text using big_title_font parameters
        drawer.draw_string(
            x=centered_x_page1_line2,
            y=295,
            text=text_page1_line2,
            font=big_title_font['font'],
            font_size=big_title_font['font_size'],
            color=big_title_font['color']
        )

    # ============================================================
    # PAGE 2
    # ============================================================
    # Upload images only on page 2
    # page_number == 1 means this is the second page
    if page_number == 1:
        # Upload company logo on page 2
        # Same width and height as page 1, same y position, x=430
        drawer.upload_image(
            image="p1/company.jpg",
            x=430,
            y=740,
            width=120,
            height=40
        )
        
        # Draw centered text "员工抗压力" on page 2
        # Get canvas object to calculate text width for centering
        canvas_obj = pdf.get_canvas()
        text_page2_line1 = "员工抗压力"
        # Calculate text width to center it using big_title_font parameters
        text_width_page2_line1 = canvas_obj.stringWidth(
            text_page2_line1, big_title_font['font'], big_title_font['font_size'])
        # Calculate centered x position
        centered_x_page2_line1 = (page_width - text_width_page2_line1) / 2
        # Draw the centered text using big_title_font parameters
        drawer.draw_string(
            x=centered_x_page2_line1,
            y=625,
            text=text_page2_line1,
            font=big_title_font['font'],
            font_size=big_title_font['font_size'],
            color=big_title_font['color']
        )

        # Draw centered text "和岗位胜任力报告" on page 2
        text_page2_line2 = "和岗位胜任力报告"
        # Calculate text width to center it using big_title_font parameters
        text_width_page2_line2 = canvas_obj.stringWidth(
            text_page2_line2, big_title_font['font'], big_title_font['font_size'])
        # Calculate centered x position
        centered_x_page2_line2 = (page_width - text_width_page2_line2) / 2
        # Draw the centered text using big_title_font parameters
        drawer.draw_string(
            x=centered_x_page2_line2,
            y=580,
            text=text_page2_line2,
            font=big_title_font['font'],
            font_size=big_title_font['font_size'],
            color=big_title_font['color']
        )

        # Add centered text on page 2 (moved from page 1)
        # Get canvas object to calculate text width for centering
        canvas_obj = pdf.get_canvas()

        # Draw first centered text at y=120
        # Using page2_text_font object parameters
        # Text: "测评单位（测评师）：中科宜和（北京）"
        text1 = "测评单位（测评师）：中科宜和（北京）"
        # Calculate text width to center it
        # stringWidth() measures how wide the text will be
        text_width1 = canvas_obj.stringWidth(
            text1, page2_text_font['font'], page2_text_font['font_size'])
        # Calculate centered x position: (page_width - text_width) / 2
        centered_x1 = (page_width - text_width1) / 2
        # Draw the centered text using page2_text_font parameters
        drawer.draw_string(
            x=centered_x1,
            y=120,
            text=text1,
            font=page2_text_font['font'],
            font_size=page2_text_font['font_size'],
            color=page2_text_font['color']
        )

        # Draw second centered text at y=95
        # Using page2_text_font object parameters
        # Text: "测评地点：北京市 / 北京市 / 海淀区"
        text2 = "测评地点：北京市 / 北京市 / 海淀区"
        # Calculate text width to center it
        text_width2 = canvas_obj.stringWidth(
            text2, page2_text_font['font'], page2_text_font['font_size'])
        # Calculate centered x position
        centered_x2 = (page_width - text_width2) / 2
        # Draw the centered text using page2_text_font parameters
        drawer.draw_string(
            x=centered_x2,
            y=95,
            text=text2,
            font=page2_text_font['font'],
            font_size=page2_text_font['font_size'],
            color=page2_text_font['color']
        )

    # ============================================================
    # PAGE 3 - SPECIFIC CONTENT
    # ============================================================
    # Add title text on page 3 only
    # page_number == 2 means this is page 3
    if page_number == 2:
        # Draw "心理韧性测评报告" at position (50, 740) using title font
        drawer.draw_string(
            x=50,
            y=740,
            text="心理韧性测评报告",
            font=chinese_title_font['font'],
            font_size=chinese_title_font['font_size'],
            color=chinese_title_font['color']
        )
        
        # Draw "GENERAL ABILITY REPORT" at position (50, 715) using English title font
        drawer.draw_string(
            x=50,
            y=715,
            text="GENERAL ABILITY REPORT",
            font=english_title_font['font'],
            font_size=english_title_font['font_size'],
            color=english_title_font['color']
        )
        
        # Get canvas object for drawing and calculating widths
        canvas_obj = pdf.get_canvas()
        
        # Use paragraph_title function to draw "心理韧性 | Psychological Resilience"
        draw_paragraph_title(drawer, canvas_obj, 50, 670, "心理韧性", "Psychological Resilience")
        
        # Draw justified paragraph at (50, 650) with wrap width 345, height 70
        # Create paragraph style for justified text
        paragraph_text = """心理韧性（Resilience）是指个体在面对压力、逆境、创伤或重大生活挑战时能够良好适应、快速恢复并从中成长的能力。它反映了一个人在情绪、认知和行为层面的抗压能力与自我调节能力。高心理韧性者通常更乐观、适应力强、能有效应对不确定性。"""
        
        # Register Chinese font for reportlab
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        
        # Create custom paragraph style with justified alignment
        paragraph_style = ParagraphStyle(
            'CustomJustified',
            fontName='STSong-Light',
            fontSize=text_font['font_size'],
            textColor=colors.Color(text_font['color'][0], text_font['color'][1], text_font['color'][2]),
            alignment=TA_JUSTIFY,
            leading=text_font['font_size'] * 1.2  # Line height
        )
        
        # Create paragraph object
        para = Paragraph(paragraph_text, paragraph_style)
        
        # Wrap and draw the paragraph
        para.wrapOn(canvas_obj, 345, 70)
        para.drawOn(canvas_obj, 50, 650 - 70)  # Subtract height for top-to-bottom positioning
        
        # Add explainparagraph image at (430, 630) with width 130, height 80
        drawer.upload_image(
            image="p3/explainparagraph.png",
            x=430,
            y=630,
            width=130,
            height=80
        )
        
        # Add dottedline image at (50, 565)
        drawer.upload_image(
            image="p3/dottedline.png",
            x=50,
            y=565,
            width=495,
            height=2
        )
        
        # Add paragraph title "测评结果详情 | Results Details" at (50, 525)
        draw_paragraph_title(drawer, canvas_obj, 50, 525, "测评结果详情", "Results Details")
        
        # Add graph image at (80, 390) - height decreased by 100 pts
        drawer.upload_image(
            image="p3/graph.png",
            x=80,
            y=390,
            width=435,
            height=10
        )
        
        # Add dottedline image at (50, 300)
        drawer.upload_image(
            image="p3/dottedline.png",
            x=50,
            y=300,
            width=495,
            height=2
        )
        
        # Add paragraph title "心理韧性等级说明 | Applications" at (50, 260)
        draw_paragraph_title(drawer, canvas_obj, 50, 260, "心理韧性等级说明", "Applications")
        
        # Add bottomparagraph image at (50, 90) with width 495, height 150
        drawer.upload_image(
            image="p3/bottomparagraph.png",
            x=50,
            y=90,
            width=495,
            height=150
        )

    # ============================================================
    # PAGE 4 - SPECIFIC CONTENT
    # ============================================================
    # Add content only on page 4
    # page_number == 3 means this is page 4
    if page_number == 3:
        # Calculate paragraph width: page_width - (2 x 50)
        paragraph_width = page_width - 100
        
        # Upload paragraph1 image at (50, 480) with calculated width, height 320
        drawer.upload_image(
            image="p4/paragraph1.png",
            x=50,
            y=480,
            width=paragraph_width,
            height=320
        )
        
        # Upload paragraph2 image at (50, 50) with same width and height as paragraph1
        drawer.upload_image(
            image="p4/paragraph2.png",
            x=50,
            y=50,
            width=paragraph_width,
            height=320
        )

    # ============================================================
    # PAGE 5 - SPECIFIC CONTENT
    # ============================================================
    # Add content only on page 5
    # page_number == 4 means this is page 5
    if page_number == 4:
        # Upload paragraph1 image at (100, 430) with width 510, height 330 (760-430)
        drawer.upload_image(
            image="p5/paragraph1.png",
            x=100,
            y=430,
            width=510,
            height=330
        )
        
        # Upload paragraph2 image at (100, 60) with width 500, height 330 (380-50)
        drawer.upload_image(
            image="p5/paragraph2.png",
            x=100,
            y=60,
            width=500,
            height=330
        )

    # ============================================================
    # PAGE 6 - SPECIFIC CONTENT
    # ============================================================
    # Add content only on page 6
    # page_number == 5 means this is page 6
    if page_number == 5:
        # Calculate paragraph width: page_width - 100
        paragraph_width = page_width - 100
        
        # Upload paragraph1 image at (50, 240) with calculated width, height 500 (760-260)
        drawer.upload_image(
            image="p6/paragraph1.png",
            x=50,
            y=240,
            width=paragraph_width,
            height=500
        )

    # ============================================================
    # PAGE 7 - SPECIFIC CONTENT
    # ============================================================
    # Add content only on page 7
    # page_number == 6 means this is page 7
    if page_number == 6:
        # Get canvas object for drawing
        canvas_obj = pdf.get_canvas()
        
        # Draw Chinese title "人格特质测试报告" at same location as previous Chinese titles
        draw_chinese_title(drawer, 50, 740, "人格特质测试报告")
        
        # Draw English title "Basic Psychological Traits" at same location as previous English titles
        draw_english_title(drawer, 50, 715, "Basic Psychological Traits")
        
        # Draw Chinese subtitle at y=685 with font size reduced by 5 pts (27-5=22)
        draw_chinese_title(drawer, 50, 685, "大五人格量表（ CBF-P1-15）", font_size=22)
        
        # Draw English subtitle at y=680 with Helvetica font
        draw_english_title(drawer, 50, 680, "Chinese Big Personality Inventory-15", font_size=22, font="Helvetica")
        
        # Draw paragraph at (50, 630) with width 345, height 70
        paragraph_text = """大五人格 (The Big Five Personality Traits) 是描述人类性格最广泛接受的模型之一，包含五个核心维度：神经质、外倾性、开放性、宜人性和尽责性。了解自己的人格特质有助于更好地认识自我，提升人际关系，优化发展路径。"""
        draw_paragraph(canvas_obj, 50, 630, 345, 70, paragraph_text)
        
        # Upload explainparagraph/points image at (410, 630) with same dimensions as page 3
        drawer.upload_image(
            image="p7/points.png",
            x=410,
            y=630,
            width=130,
            height=80
        )
        
        # Add dottedline image at (50, 565)
        drawer.upload_image(
            image="p3/dottedline.png",
            x=50,
            y=565,
            width=495,
            height=2
        )
        
        # Call subtitle function at (50, 550)
        draw_paragraph_title(drawer, canvas_obj, 50, 550, "我的人格特质类型", "My Big Personality")
        
        # Upload paragraph2 image at (50, 60) with height 160, width = page_width - 300
        drawer.upload_image(
            image="p7/paragraph2.png",
            x=50,
            y=60,
            width=page_width - 300,
            height=160
        )

    # ============================================================
    # PAGE 3+ - CONTENT PAGES
    # ============================================================
    # Add page number and title text on pages 3 and beyond
    # page_number >= 2 means page 3 or later
    if page_number >= 2:
        # Draw page number
        # Position: x=50, y=25 (bottom left area)
        # Font size: 9 (decreased by 1pt), black, STSong-Light
        drawer.draw_string(
            x=50,
            y=25,
            text=str(page_counter),
            font="STSong-Light",
            font_size=9,
            color=Colors.BLACK
        )
        
        # Draw footer title text with reduced spacing (10pts less space)
        # Previously 20 spaces, now reduced spacing between number and text
        drawer.draw_string(
            x=70,  # 20pts after page number start (reduced from 30pts)
            y=25,
            text="员工抗压力和岗位胜任力报告",
            font="STSong-Light",
            font_size=9,
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
