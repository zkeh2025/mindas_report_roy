# Import modules
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
from roy_pdf_library import PDFGenerator, PDFDrawer, Colors, create_pdf

# Change to the script's directory to ensure relative paths work
# This makes sure image files can be found regardless of where the script is run from
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

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

# Register custom fonts
from reportlab.pdfbase.ttfonts import TTFont

# Register all fonts from 字体 folder
pdfmetrics.registerFont(TTFont('FZLanTingXiHei', '字体/FZLTXHK 2.TTF'))  # 方正兰亭细黑
pdfmetrics.registerFont(TTFont('FZLanTingTeHei', '字体/FZLTTHK.TTF'))  # 方正兰亭特黑 (Bold)
pdfmetrics.registerFont(TTFont('FZLanTingCuHei', '字体/FZLTZCHJW.TTF'))  # 方正兰亭粗黑加粗
pdfmetrics.registerFont(TTFont('FZLanTingChaoHei', '字体/FZLTCHK.ttf'))  # 方正兰亭超黑
pdfmetrics.registerFont(TTFont('FZLanTingHei4', '字体/FZLTH4K.TTF'))  # 方正兰亭黑4
# pdfmetrics.registerFont(TTFont('FZLanTingZhunHei', '字体/FZLTZHUNHK_0.otf'))  # 方正兰亭准黑 - OTF with PostScript outlines not supported
pdfmetrics.registerFont(TTFont('FZTianYiSongK', '字体/FZTYSK.TTF'))  # 方正天一宋
pdfmetrics.registerFont(TTFont('Impact', '字体/impact.ttf'))  # Impact

# Define color constants
deepblue = [49/255, 92/255, 170/255]  # RGB color for pentagon text

# Define variables for text
teacher = "张老师"  # Teacher name variable
location = "北京"   # Location variable
location_province = "北京市"  # Province variable
district = "海淀区"  # District variable

# Define pentagon score variables (1-5 representing layers from innermost to outermost)
E_score = 3  # Extraversion score
A_score = 4  # Agreeableness score
C_score = 2  # Conscientiousness score
N_score = 5  # Neuroticism score
O_score = 4  # Openness score

# Define resilience score variable
resilience_score = 85  # Resilience score (0-100)

# Define stress coping score variable
stress_coping_score = 72  # Stress coping score (0-100)

# Define page 9 coping strategy scores
problem_solve_score = 45  # Problem solving score
doubt_score = 30  # Doubt score
help_score = 35  # Help seeking score
fantasy_score = 25  # Fantasy score
escape_score = 20  # Escape score
rationalization_score = 40  # Rationalization score

# Define rectangle colors for page 9 bar chart
rect_color_1 = [0.2, 0.6, 0.8]  # Light blue for problem solving
rect_color_2 = [0.8, 0.4, 0.4]  # Light red for doubt
rect_color_3 = [0.4, 0.8, 0.4]  # Light green for help
rect_color_4 = [0.9, 0.7, 0.3]  # Yellow for fantasy
rect_color_5 = [0.7, 0.5, 0.8]  # Purple for escape
rect_color_6 = [0.9, 0.5, 0.3]  # Orange for rationalization

# Define personality_graph module to draw 5-layered pentagon
def draw_personality_graph(canvas_obj, center_x, center_y):
    """
    Draw a 5-layered pentagon (radar chart) for personality traits
    Parameters:
        canvas_obj: Canvas object for drawing
        center_x: x position of center
        center_y: y position of center
    """
    import math
    
    # Calculate pentagon vertices for each of 5 layers
    # Each layer increases distance by 15 pts: 32, 47, 62, 77, 92
    distances = [32, 47, 62, 77, 92]
    
    # Pentagon has 5 vertices at angles: 90°, 162°, 234°, 306°, 18° (starting from top, clockwise)
    # Or: 90°, 18°, 306°, 234°, 162° (top, top-right, bottom-right, bottom-left, top-left)
    angles_degrees = [90, 18, 306, 234, 162]  # Starting from top, going clockwise
    angles_radians = [math.radians(a) for a in angles_degrees]
    
    # Store all vertices for each layer
    layers = []
    for distance in distances:
        layer_vertices = []
        for angle in angles_radians:
            x = center_x + distance * math.cos(angle)
            y = center_y + distance * math.sin(angle)
            layer_vertices.append((x, y))
        layers.append(layer_vertices)
    
    # Draw pentagons from outer to inner (layers 4 to 0)
    # Set deep blue color for lines
    canvas_obj.setStrokeColorRGB(deepblue[0], deepblue[1], deepblue[2])  # Deep blue
    canvas_obj.setLineWidth(0.3)  # Line width 0.3
    
    # Draw each pentagon layer
    for layer_idx in range(4, -1, -1):  # 4, 3, 2, 1, 0 (outermost to innermost)
        vertices = layers[layer_idx]
        
        # Create path for pentagon
        path = canvas_obj.beginPath()
        
        # Move to first vertex
        path.moveTo(vertices[0][0], vertices[0][1])
        
        # Draw lines to other vertices
        for i in range(1, 5):
            path.lineTo(vertices[i][0], vertices[i][1])
        
        # Close the pentagon
        path.close()
        
        # Draw the path
        canvas_obj.drawPath(path, stroke=1, fill=0)
    
    # Return all layers for text positioning and score plotting
    return layers  # Return all 5 layers

# Define function to draw pentagon text labels
def draw_pentagon_text(canvas_obj, text, alignment, x, y):
    """
    Draw text label for pentagon vertices
    Parameters:
        canvas_obj: Canvas object for drawing
        text: Text content to draw
        alignment: 'left', 'center', or 'right'
        x: x position
        y: y position
    """
    canvas_obj.setFont('FZLanTingTeHei', 9.32)  # Using bold font (特黑)
    canvas_obj.setFillColorRGB(deepblue[0], deepblue[1], deepblue[2])
    
    if alignment == 'center':
        canvas_obj.drawCentredString(x, y, text)
    elif alignment == 'right':
        canvas_obj.drawRightString(x, y, text)
    else:  # left alignment (default)
        canvas_obj.drawString(x, y, text)

# Define function to draw score text under pentagon labels
def draw_pentagon_score_text(canvas_obj, score, alignment, x, y):
    """
    Draw score text (e.g., "(3/5)") under pentagon vertex label
    Parameters:
        canvas_obj: Canvas object for drawing
        score: Score value (1-5)
        alignment: 'left', 'center', or 'right'
        x: x position
        y: y position (will draw below this)
    """
    canvas_obj.setFont('FZLanTingTeHei', 8)  # Slightly smaller font for score
    canvas_obj.setFillColorRGB(deepblue[0], deepblue[1], deepblue[2])
    
    score_text = f"({score}/5)"
    y_offset = y - 12  # Draw 12pts below the main text
    
    if alignment == 'center':
        canvas_obj.drawCentredString(x, y_offset, score_text)
    elif alignment == 'right':
        canvas_obj.drawRightString(x, y_offset, score_text)
    else:  # left alignment (default)
        canvas_obj.drawString(x, y_offset, score_text)

# Define function to print score number
def print_score(canvas_obj, score, x, y):
    """
    Print score number with Impact font
    Parameters:
        canvas_obj: Canvas object for drawing
        score: Score value to display
        x: x position
        y: y position
    """
    canvas_obj.setFont('Impact', 40)
    canvas_obj.setFillColorRGB(deepblue[0], deepblue[1], deepblue[2])
    canvas_obj.drawString(x, y, str(score))

# Define function to draw orange lines with labels for page 9
def draw_orange_lines(canvas_obj):
    """
    Draw horizontal orange lines with score labels for page 9 bar chart
    Parameters:
        canvas_obj: Canvas object for drawing
    """
    orange = [1.0, 0.63922, 0.0]
    counter = 0
    
    while counter <= 5:
        # Calculate y position for this line
        y_pos = 300 + (counter * 40)
        
        # Draw orange horizontal line
        canvas_obj.setStrokeColorRGB(orange[0], orange[1], orange[2], alpha=1)
        canvas_obj.setLineWidth(1)
        canvas_obj.line(100, y_pos, 500, y_pos)  # length = 400 (from x=100 to x=500)
        
        # Print score label (counter * 40)
        score_label = counter * 40
        canvas_obj.setFont('FZLanTingXiHei', 12)
        canvas_obj.setFillColorRGB(0, 0, 0)
        canvas_obj.drawString(90, y_pos, str(score_label))
        
        counter += 1

# Define functions to draw bar charts for each coping strategy
def problem_solve_draw(canvas_obj, drawer, score, color, base_x, base_y):
    """
    Draw bar chart for problem solving score
    """
    # Draw rectangle
    rect_height = score * 4
    rect_width = 25
    drawer.draw_rect(
        pos_x=base_x + 20,
        pos_y=base_y,
        width=rect_width,
        height=rect_height,
        color=color,
        fill=1,
        stroke=0
    )
    
    # Draw score text above rectangle
    canvas_obj.setFont('FZLanTingXiHei', 12)
    canvas_obj.setFillColorRGB(0, 0, 0)
    text_x = base_x + 20 + (rect_width / 2)
    text_y = base_y + rect_height + 10
    canvas_obj.drawCentredString(text_x, text_y, str(score))

def doubt_draw(canvas_obj, drawer, score, color, base_x, base_y):
    """
    Draw bar chart for doubt score
    """
    rect_height = score * 4
    rect_width = 25
    drawer.draw_rect(
        pos_x=base_x + 20,
        pos_y=base_y,
        width=rect_width,
        height=rect_height,
        color=color,
        fill=1,
        stroke=0
    )
    canvas_obj.setFont('FZLanTingXiHei', 12)
    canvas_obj.setFillColorRGB(0, 0, 0)
    text_x = base_x + 20 + (rect_width / 2)
    text_y = base_y + rect_height + 10
    canvas_obj.drawCentredString(text_x, text_y, str(score))

def help_draw(canvas_obj, drawer, score, color, base_x, base_y):
    """
    Draw bar chart for help seeking score
    """
    rect_height = score * 4
    rect_width = 25
    drawer.draw_rect(
        pos_x=base_x + 20,
        pos_y=base_y,
        width=rect_width,
        height=rect_height,
        color=color,
        fill=1,
        stroke=0
    )
    canvas_obj.setFont('FZLanTingXiHei', 12)
    canvas_obj.setFillColorRGB(0, 0, 0)
    text_x = base_x + 20 + (rect_width / 2)
    text_y = base_y + rect_height + 10
    canvas_obj.drawCentredString(text_x, text_y, str(score))

def fantasy_draw(canvas_obj, drawer, score, color, base_x, base_y):
    """
    Draw bar chart for fantasy score
    """
    rect_height = score * 4
    rect_width = 25
    drawer.draw_rect(
        pos_x=base_x + 20,
        pos_y=base_y,
        width=rect_width,
        height=rect_height,
        color=color,
        fill=1,
        stroke=0
    )
    canvas_obj.setFont('FZLanTingXiHei', 12)
    canvas_obj.setFillColorRGB(0, 0, 0)
    text_x = base_x + 20 + (rect_width / 2)
    text_y = base_y + rect_height + 10
    canvas_obj.drawCentredString(text_x, text_y, str(score))

def escape_draw(canvas_obj, drawer, score, color, base_x, base_y):
    """
    Draw bar chart for escape score
    """
    rect_height = score * 4
    rect_width = 25
    drawer.draw_rect(
        pos_x=base_x + 20,
        pos_y=base_y,
        width=rect_width,
        height=rect_height,
        color=color,
        fill=1,
        stroke=0
    )
    canvas_obj.setFont('FZLanTingXiHei', 12)
    canvas_obj.setFillColorRGB(0, 0, 0)
    text_x = base_x + 20 + (rect_width / 2)
    text_y = base_y + rect_height + 10
    canvas_obj.drawCentredString(text_x, text_y, str(score))

def rationalization_draw(canvas_obj, drawer, score, color, base_x, base_y):
    """
    Draw bar chart for rationalization score
    """
    rect_height = score * 4
    rect_width = 25
    drawer.draw_rect(
        pos_x=base_x + 20,
        pos_y=base_y,
        width=rect_width,
        height=rect_height,
        color=color,
        fill=1,
        stroke=0
    )
    canvas_obj.setFont('FZLanTingXiHei', 12)
    canvas_obj.setFillColorRGB(0, 0, 0)
    text_x = base_x + 20 + (rect_width / 2)
    text_y = base_y + rect_height + 10
    canvas_obj.drawCentredString(text_x, text_y, str(score))

# Define function to find min and max scores
def find_min_max_scores(E, A, C, N, O):
    """
    Find the minimum and maximum scores from the 5 personality traits
    Parameters:
        E, A, C, N, O: Score values for each trait
    Returns:
        Tuple of (min_score, max_score)
    """
    scores = [E, A, C, N, O]
    min_score = min(scores)
    max_score = max(scores)
    return min_score, max_score

# Define function to find vertex position based on score
def get_vertex_for_score(layers, vertex_index, score, score_name):
    """
    Find the vertex position for a given score
    Parameters:
        layers: List of all pentagon layers
        vertex_index: Which vertex (0=top/E, 1=top-right/O, 2=bottom-right/N, 3=bottom-left/C, 4=top-left/A)
        score: Score value (1-5)
        score_name: Name of the score for error messages
    Returns:
        Tuple of (x, y) coordinates
    """
    counter = 1
    for i in range(5):  # Check 5 layers
        if score == counter:
            # Found matching layer, return the vertex
            layer_idx = counter - 1  # Convert score (1-5) to layer index (0-4)
            return layers[layer_idx][vertex_index]
        counter += 1
    
    # If we get here, score was not 1-5
    print(f"Error: {score_name} value {score} is invalid. Must be between 1 and 5.")
    return None

# Define function to draw score dots and connect them
def draw_pentagon_scores(canvas_obj, layers, E, A, C, N, O):
    """
    Draw dots at score positions and connect them with lines
    Parameters:
        canvas_obj: Canvas object
        layers: All pentagon layers
        E, A, C, N, O: Score values for each trait
    """
    # Define orange color for lines
    orange = [1.0, 0.63922, 0.0]
    
    # Get vertex positions for each score
    # vertex_index: 0=top(E), 1=top-right(O), 2=bottom-right(N), 3=bottom-left(C), 4=top-left(A)
    E_pos = get_vertex_for_score(layers, 0, E, "E_score")
    A_pos = get_vertex_for_score(layers, 4, A, "A_score")
    C_pos = get_vertex_for_score(layers, 3, C, "C_score")
    N_pos = get_vertex_for_score(layers, 2, N, "N_score")
    O_pos = get_vertex_for_score(layers, 1, O, "O_score")
    
    # Check if all positions are valid
    positions = [E_pos, A_pos, O_pos, N_pos, C_pos]
    if None in positions:
        return  # Error occurred, don't draw
    
    # Draw connecting lines between dots (in order: E -> O -> N -> C -> A -> back to E)
    canvas_obj.setStrokeColorRGB(orange[0], orange[1], orange[2], alpha=1)
    canvas_obj.setLineWidth(2)
    
    # Connect: E -> O -> N -> C -> A -> E (forming a closed shape)
    line_order = [E_pos, O_pos, N_pos, C_pos, A_pos, E_pos]
    for i in range(len(line_order) - 1):
        canvas_obj.line(line_order[i][0], line_order[i][1], 
                       line_order[i+1][0], line_order[i+1][1])
    
    # Draw dots at each position
    canvas_obj.setFillColorRGB(orange[0], orange[1], orange[2], alpha=1)
    dot_radius = 3
    for pos in positions:
        canvas_obj.circle(pos[0], pos[1], dot_radius, stroke=0, fill=1)

# Define function to draw white rectangle
def draw_white_rectangle(drawer, x, y, width, height):
    """
    Draw a white filled rectangle with no border
    Parameters:
        drawer: PDFDrawer object
        x: x position (left edge)
        y: y position (bottom edge)
        width: rectangle width
        height: rectangle height
    """
    drawer.draw_rect(
        pos_x=x,
        pos_y=y,
        width=width,
        height=height,
        color=Colors.WHITE,
        fill=1,
        stroke=0
    )

# Define function to draw centered text with paragraph
def draw_big_text(canvas_obj, x, y, text, width):
    """
    Draw centered text with FZLanTingXiHei font
    Parameters:
        canvas_obj: Canvas object
        x: x position (left edge of text box)
        y: y position (top of text box)
        text: text content to draw
        width: width of text box for wrapping
    """
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import Paragraph
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib import colors as reportlab_colors
    
    # Create paragraph style with specified font
    style = ParagraphStyle(
        name='CustomStyle',
        fontName='FZLanTingXiHei',
        fontSize=14,
        leading=14 * 1.2,  # leading = fontSize * 1.2
        alignment=TA_LEFT,
        textColor=reportlab_colors.black,
    )
    
    # Create paragraph with text
    para = Paragraph(text, style)
    
    # Calculate width and height needed
    para_width, para_height = para.wrap(width, 100)
    
    # Draw paragraph at specified position
    para.drawOn(canvas_obj, x, y - para_height)

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

    # ============================================================
    # PAGE UPLOAD MODULE - Upload full-page background images
    # ============================================================
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

    # ============================================================
    # EDITS MODULE - All edits applied after page upload
    # ============================================================
    
    # PAGE 1 - Draw full-width white rectangle
    if page_number == 0:
        draw_white_rectangle(drawer, x=0, y=310, width=page_width, height=220)
    
    # Draw white filled rectangle (no border) only on pages 3, 7 (removed from page 2)
    if page_number in [2, 6]:  # pages 3, 7
        draw_white_rectangle(drawer, x=160, y=310, width=300, height=220)

    # PAGE 2 - Draw white rectangle and text
    # page_number == 1 means this is page 2
    if page_number == 1:
        # Draw white rectangle at specified position (increased width by 100, moved 50 to right)
        draw_white_rectangle(drawer, x=190, y=60, width=360, height=440)
        
        # Get canvas object for drawing text
        canvas_obj = pdf.get_canvas()
        
        # Format text with variables and spacing (reduced from 5pts to 3pts)
        # 测评单位 + 3pts space + （teacher） + : + 3pts space + 中科宜和(location)
        formatted_text = f'测评单位   （{teacher}）:   中科宜和（{location}）'
        
        # Calculate center x position for centered text
        center_x = page_width / 2
        
        # Draw centered text at y=120 using canvas's drawCentredString
        canvas_obj.setFont('FZLanTingXiHei', 14)
        canvas_obj.setFillColorRGB(0, 0, 0)
        canvas_obj.drawCentredString(center_x, 120, formatted_text)
        
        # Draw location text with province, location, and district
        # 测评地点,: + 3pts space + location_province / location / district (reduced from 5pts to 3pts)
        location_text = f'测评地点,:   {location_province}/{location}/{district}'
        
        # Draw centered text at y=100 using canvas's drawCentredString
        canvas_obj.setFont('FZLanTingXiHei', 14)
        canvas_obj.setFillColorRGB(0, 0, 0)
        canvas_obj.drawCentredString(center_x, 100, location_text)
        
        # Print resilience score in top right corner rectangle
        print_score(canvas_obj, resilience_score, 190 + 20, 60 + 440 + 10)

    # PAGE 3 - Draw white rectangle
    # page_number == 2 means this is page 3
    if page_number == 2:
        # Draw white rectangle at specified position
        draw_white_rectangle(drawer, x=450, y=665, width=80, height=45)

    # PAGE 9 - Draw white rectangles, stress coping score, and bar charts
    # page_number == 8 means this is page 9
    if page_number == 8:
        # Draw white rectangle at specified position for stress coping score
        draw_white_rectangle(drawer, x=450, y=670, width=40, height=60)
        
        # Draw white rectangle for bar chart area
        draw_white_rectangle(drawer, x=60, y=280, width=470, height=230)
        
        # Get canvas object for drawing
        canvas_obj = pdf.get_canvas()
        
        # Print stress coping score
        print_score(canvas_obj, stress_coping_score, 450 + 30, 670)
        
        # Draw orange lines with labels
        draw_orange_lines(canvas_obj)
        
        # Draw bar charts for all 6 coping strategies
        # Base positions for each bar (evenly spaced across chart)
        base_y = 300  # Starting y position (same as first orange line)
        spacing = 60  # Space between bars
        
        problem_solve_draw(canvas_obj, drawer, problem_solve_score, rect_color_1, 100 + (spacing * 0), base_y)
        doubt_draw(canvas_obj, drawer, doubt_score, rect_color_2, 100 + (spacing * 1), base_y)
        help_draw(canvas_obj, drawer, help_score, rect_color_3, 100 + (spacing * 2), base_y)
        fantasy_draw(canvas_obj, drawer, fantasy_score, rect_color_4, 100 + (spacing * 3), base_y)
        escape_draw(canvas_obj, drawer, escape_score, rect_color_5, 100 + (spacing * 4), base_y)
        rationalization_draw(canvas_obj, drawer, rationalization_score, rect_color_6, 100 + (spacing * 5), base_y)

    # PAGE 7 - Draw pentagon graph (on top of rectangle)
    # page_number == 6 means this is page 7
    if page_number == 6:
        # Draw white rectangles on page 7
        draw_white_rectangle(drawer, x=430, y=650, width=40, height=60)
        draw_white_rectangle(drawer, x=490, y=650, width=40, height=60)
        
        # Get canvas object for drawing
        canvas_obj = pdf.get_canvas()
        
        # Draw personality graph (5-layered pentagon) at center position (300, 400) - moved 20pts down
        all_layers = draw_personality_graph(canvas_obj, 300, 400)
        
        # Get outermost layer for text labels
        vertices = all_layers[4]  # Layer 5 (outermost)
        
        # vertices order: [top, top-right, bottom-right, bottom-left, top-left]
        # vertices[0] = top (90°)
        # vertices[1] = top-right (18°)
        # vertices[2] = bottom-right (306°)
        # vertices[3] = bottom-left (234°)
        # vertices[4] = top-left (162°)
        
        # Draw score dots and connecting lines
        draw_pentagon_scores(canvas_obj, all_layers, E_score, A_score, C_score, N_score, O_score)
        
        # Define text positions and scores for all 5 traits
        # Format: (text, score, alignment, x, y)
        text_data = [
            ('外倾性 E', E_score, 'center', vertices[0][0], vertices[0][1] + 15),  # Top
            ('宜人性 A', A_score, 'left', vertices[4][0] - 10, vertices[4][1]),    # Top-left
            ('开放性 O', O_score, 'left', vertices[1][0] + 15, vertices[1][1]),    # Top-right
            ('尽责性 C', C_score, 'left', vertices[3][0] - 25, vertices[3][1] - 15),  # Bottom-left
            ('神经质 N', N_score, 'left', vertices[2][0] + 15, vertices[2][1] - 10)   # Bottom-right
        ]
        
        # Draw text labels and scores for each vertex using loop
        for text, score, alignment, x, y in text_data:
            draw_pentagon_text(canvas_obj, text, alignment, x, y)
            draw_pentagon_score_text(canvas_obj, score, alignment, x, y)
        
        # Find min and max scores from pentagon variables
        min_score, max_score = find_min_max_scores(E_score, A_score, C_score, N_score, O_score)
        
        # Print max_score in leftmost top right rectangle
        print_score(canvas_obj, max_score, 430 + 10, 650 + 60 + 20)
        
        # Print min_score 25pts to the right of max_score
        print_score(canvas_obj, min_score, 430 + 10 + 25, 650 + 60 + 20)

    # ============================================================
    # RULER MODULE - Draw ruler on TOP of everything
    # ============================================================
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
