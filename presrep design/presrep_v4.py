# Import modules
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from pdf_generate_api.roy_pdf_library import (
    PDFGenerator,
    PDFDrawer,
    Colors,
    create_pdf,
)

# Change to the script's directory to ensure relative paths work
# This makes sure image files can be found regardless of where the script is run from
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Create PDF with A4 page size
# A4 = standard paper size (210mm x 297mm)
# pagesize=A4 tells the PDF generator to use A4 dimensions
pdf = create_pdf("presrep_output_v4.pdf", pagesize=A4)

# Get the drawer object to draw on the PDF
drawer = pdf.get_drawer()

# Define page dimensions for A4
# mm = millimeter units (converts mm to points for PDF)
page_width = 210 * mm   # A4 width = 210 millimeters
page_height = 297 * mm  # A4 height = 297 millimeters

# Register custom fonts
from reportlab.pdfbase.ttfonts import TTFont

# Register all fonts from 字体 folder
font_base_path = "pdf_generate_api/字体/"
pdfmetrics.registerFont(TTFont('FZLanTingXiHei', font_base_path + 'FZLTXHK 2.TTF'))  # 方正兰亭细黑
pdfmetrics.registerFont(TTFont('FZLanTingTeHei', font_base_path + 'FZLTTHK.TTF'))  # 方正兰亭特黑 (Bold)
pdfmetrics.registerFont(TTFont('FZLanTingCuHei', font_base_path + 'FZLTZCHJW.TTF'))  # 方正兰亭粗黑加粗
pdfmetrics.registerFont(TTFont('FZLanTingChaoHei', font_base_path + 'FZLTCHK.ttf'))  # 方正兰亭超黑
pdfmetrics.registerFont(TTFont('FZLanTingHei4', font_base_path + 'FZLTH4K.TTF'))  # 方正兰亭黑4
# pdfmetrics.registerFont(TTFont('FZLanTingZhunHei', font_base_path + 'FZLTZHUNHK_0.otf'))  # 方正兰亭准黑 - OTF with PostScript outlines not supported
pdfmetrics.registerFont(TTFont('FZTianYiSongK', font_base_path + 'FZTYSK.TTF'))  # 方正天一宋
pdfmetrics.registerFont(TTFont('Impact', font_base_path + 'impact.ttf'))  # Impact

# Define color constants
deepblue = [49/255, 92/255, 170/255]  # RGB color for pentagon text

# Define variables for text
teacher = "张老师"  # Teacher name variable
location = "北京"   # Location variable
location_province = "北京市"  # Province variable
district = "海淀区"  # District variable

# Define personal information for page 2 table
student_name = "张三"
student_sex = "男"
student_birth_date = "2000年1月1日"
student_test_date = "2023年12月1日"
student_age = "16岁"
student_school = "中国高中"
student_phone = "12345678901"

# Define page 3 and page 9 score display dimensions
score_background_width = 80
score_background_height = 65

# Define page 9 paragraph placeholders
text_1 = ""
text_2 = ""
text_3 = ""
text_4 = ""
text_5 = ""
text_6 = ""

# Define page 11 competency variables
attrativeness_score = 120.75
leadership_score = 150.60
leadership_skill_score = 210.45
competency_score = attrativeness_score + leadership_score + leadership_skill_score

# Define technical score for page 13
technical_score = 112.35

# Communication scores for page 15
communication_score = 108.64
communication_percentile = 192.57

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

# Define page 15 competency scores (8 variables)
interpersonal_score = 105.32  # 人际关系
customer_service_score = 98.45  # 客户服务
achievement_score = 110.27  # 成就导向
thinking_score = 95.83  # 思维能力
market_sensitivity_score = 102.66  # 市场敏感力
teamwork_score = 109.12  # 团队协作
knowledge_skill_score = 107.48  # 知识与技能
influence_score = 101.05  # 影响力

# Define page 13 circle variables
points = 7  # Points value
circle_degree = points * 36  # Circle degree calculation

# Define rectangle colors for page 9 bar chart
rect_color_1 = [0.2, 0.6, 0.8]  # Light blue for problem solving
rect_color_2 = [0.8, 0.4, 0.4]  # Light red for doubt
rect_color_3 = [0.4, 0.8, 0.4]  # Light green for help
rect_color_4 = [0.9, 0.7, 0.3]  # Yellow for fantasy
rect_color_5 = [0.7, 0.5, 0.8]  # Purple for escape
rect_color_6 = [0.9, 0.5, 0.3]  # Orange for rationalization

# Additional color constants
light_grey = [0.8, 0.8, 0.8]
p15_light_grey = [0.85, 0.85, 0.85]
p11_yellow = [1.0, 0.9, 0.2]
p11_light_blue = [0.6, 0.8, 1.0]
p11_dark_blue = [0.2, 0.35, 0.7]
vertical_grey = [0.6, 0.6, 0.6]

# Define rectangle colors for page 15 competency chart (8 colors)
comp_color_1 = [0.3, 0.5, 0.9]  # Blue
comp_color_2 = [0.9, 0.3, 0.5]  # Pink
comp_color_3 = [0.5, 0.9, 0.3]  # Green
comp_color_4 = [0.9, 0.6, 0.2]  # Orange
comp_color_5 = [0.6, 0.3, 0.9]  # Purple
comp_color_6 = [0.2, 0.8, 0.8]  # Cyan
comp_color_7 = [0.9, 0.9, 0.3]  # Yellow
comp_color_8 = [0.9, 0.4, 0.7]  # Magenta

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
        
        # Print score label (counter * 20), right aligned at x=90
        score_label = counter * 20
        canvas_obj.setFont('FZLanTingXiHei', 12)
        canvas_obj.setFillColorRGB(0, 0, 0)
        canvas_obj.drawRightString(90, y_pos, str(score_label))
        
        counter += 1

# Define functions to draw bar charts for each coping strategy
def problem_solve_draw(canvas_obj, drawer, score, color, base_x, base_y,
                       width_adjust=0, x_offset=0):
    """
    Draw bar chart for problem solving score
    """
    # Draw rectangle
    rect_height = score * 4
    rect_width = 25 + width_adjust
    drawer.draw_rect(
        pos_x=base_x + 20 + x_offset,
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
    text_x = base_x + 20 + x_offset + (rect_width / 2)
    text_y = base_y + rect_height + 10
    canvas_obj.drawCentredString(text_x, text_y, str(score))

def doubt_draw(canvas_obj, drawer, score, color, base_x, base_y,
               width_adjust=0, x_offset=0):
    """
    Draw bar chart for doubt score
    """
    rect_height = score * 4
    rect_width = 25 + width_adjust
    drawer.draw_rect(
        pos_x=base_x + 20 + x_offset,
        pos_y=base_y,
        width=rect_width,
        height=rect_height,
        color=color,
        fill=1,
        stroke=0
    )
    canvas_obj.setFont('FZLanTingXiHei', 12)
    canvas_obj.setFillColorRGB(0, 0, 0)
    text_x = base_x + 20 + x_offset + (rect_width / 2)
    text_y = base_y + rect_height + 10
    canvas_obj.drawCentredString(text_x, text_y, str(score))

def help_draw(canvas_obj, drawer, score, color, base_x, base_y,
              width_adjust=0, x_offset=0):
    """
    Draw bar chart for help seeking score
    """
    rect_height = score * 4
    rect_width = 25 + width_adjust
    drawer.draw_rect(
        pos_x=base_x + 20 + x_offset,
        pos_y=base_y,
        width=rect_width,
        height=rect_height,
        color=color,
        fill=1,
        stroke=0
    )
    canvas_obj.setFont('FZLanTingXiHei', 12)
    canvas_obj.setFillColorRGB(0, 0, 0)
    text_x = base_x + 20 + x_offset + (rect_width / 2)
    text_y = base_y + rect_height + 10
    canvas_obj.drawCentredString(text_x, text_y, str(score))

def fantasy_draw(canvas_obj, drawer, score, color, base_x, base_y,
                 width_adjust=0, x_offset=0):
    """
    Draw bar chart for fantasy score
    """
    rect_height = score * 4
    rect_width = 25 + width_adjust
    drawer.draw_rect(
        pos_x=base_x + 20 + x_offset,
        pos_y=base_y,
        width=rect_width,
        height=rect_height,
        color=color,
        fill=1,
        stroke=0
    )
    canvas_obj.setFont('FZLanTingXiHei', 12)
    canvas_obj.setFillColorRGB(0, 0, 0)
    text_x = base_x + 20 + x_offset + (rect_width / 2)
    text_y = base_y + rect_height + 10
    canvas_obj.drawCentredString(text_x, text_y, str(score))

def escape_draw(canvas_obj, drawer, score, color, base_x, base_y,
                width_adjust=0, x_offset=0):
    """
    Draw bar chart for escape score
    """
    rect_height = score * 4
    rect_width = 25 + width_adjust
    drawer.draw_rect(
        pos_x=base_x + 20 + x_offset,
        pos_y=base_y,
        width=rect_width,
        height=rect_height,
        color=color,
        fill=1,
        stroke=0
    )
    canvas_obj.setFont('FZLanTingXiHei', 12)
    canvas_obj.setFillColorRGB(0, 0, 0)
    text_x = base_x + 20 + x_offset + (rect_width / 2)
    text_y = base_y + rect_height + 10
    canvas_obj.drawCentredString(text_x, text_y, str(score))

def rationalization_draw(canvas_obj, drawer, score, color, base_x, base_y,
                         width_adjust=0, x_offset=0):
    """
    Draw bar chart for rationalization score
    """
    rect_height = score * 4
    rect_width = 25 + width_adjust
    drawer.draw_rect(
        pos_x=base_x + 20 + x_offset,
        pos_y=base_y,
        width=rect_width,
        height=rect_height,
        color=color,
        fill=1,
        stroke=0
    )
    canvas_obj.setFont('FZLanTingXiHei', 12)
    canvas_obj.setFillColorRGB(0, 0, 0)
    text_x = base_x + 20 + x_offset + (rect_width / 2)
    text_y = base_y + rect_height + 10
    canvas_obj.drawCentredString(text_x, text_y, str(score))

# Define additional draw functions for page 15 (with % sign)
def competency_draw_1(canvas_obj, drawer, score, color, base_x, base_y):
    """Draw bar chart with % for competency score"""
    rect_height = score * 2  # Different scale for percentage (0-100)
    rect_width = 22
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
    canvas_obj.drawCentredString(text_x, text_y, str(score) + "%")

def competency_draw_2(canvas_obj, drawer, score, color, base_x, base_y):
    """Draw bar chart with % for competency score"""
    rect_height = score * 2
    rect_width = 22
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
    canvas_obj.drawCentredString(text_x, text_y, str(score) + "%")

def competency_draw_3(canvas_obj, drawer, score, color, base_x, base_y):
    """Draw bar chart with % for competency score"""
    rect_height = score * 2
    rect_width = 22
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
    canvas_obj.drawCentredString(text_x, text_y, str(score) + "%")

def competency_draw_4(canvas_obj, drawer, score, color, base_x, base_y):
    """Draw bar chart with % for competency score"""
    rect_height = score * 2
    rect_width = 22
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
    canvas_obj.drawCentredString(text_x, text_y, str(score) + "%")

def competency_draw_5(canvas_obj, drawer, score, color, base_x, base_y):
    """Draw bar chart with % for competency score"""
    rect_height = score * 2
    rect_width = 22
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
    canvas_obj.drawCentredString(text_x, text_y, str(score) + "%")

def competency_draw_6(canvas_obj, drawer, score, color, base_x, base_y):
    """Draw bar chart with % for competency score"""
    rect_height = score * 2
    rect_width = 22
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
    canvas_obj.drawCentredString(text_x, text_y, str(score) + "%")

def competency_draw_7(canvas_obj, drawer, score, color, base_x, base_y):
    """Draw bar chart with % for competency score"""
    rect_height = score * 2
    rect_width = 22
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
    canvas_obj.drawCentredString(text_x, text_y, str(score) + "%")

def competency_draw_8(canvas_obj, drawer, score, color, base_x, base_y):
    """Draw bar chart with % for competency score"""
    rect_height = score * 2
    rect_width = 22
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
    canvas_obj.drawCentredString(text_x, text_y, str(score) + "%")

# Define function to draw two white rectangles for page 9
def draw_two_white_rect(drawer, y, y_offset=0, right_width_adjust=5, right_x_offset=3):
    """
    Draw two white rectangles at fixed x positions
    Parameters:
        drawer: PDFDrawer object
        y: Y position for rectangles
    """
    rect_width = 200
    rect_height = 50

    adjusted_y = y + y_offset

    left_rect = (80, adjusted_y, rect_width, rect_height)
    right_rect = (330 + right_x_offset, adjusted_y, rect_width + right_width_adjust, rect_height)

    draw_white_rectangle(drawer, *left_rect)
    draw_white_rectangle(drawer, *right_rect)

    return [left_rect, right_rect]

# Define function to draw page 9 graph with orange lines and bar charts
def draw_p9_graph(canvas_obj, drawer, problem_solve_score, doubt_score, help_score, 
                  fantasy_score, escape_score, rationalization_score,
                  rect_color_1, rect_color_2, rect_color_3, rect_color_4, rect_color_5, rect_color_6):
    """
    Draw complete page 9 graph with orange lines and all 6 bar charts
    Parameters:
        canvas_obj: Canvas object for drawing
        drawer: PDFDrawer object
        All 6 scores and colors
    """
    # Draw orange lines with labels
    draw_orange_lines(canvas_obj)
    
    # Draw bar charts for all 6 coping strategies
    # Base positions for each bar (evenly spaced across chart)
    base_y = 300  # Starting y position (same as first orange line)
    spacing = 30  # Space between bars

    base_positions = [100 + (spacing * i) for i in range(6)]
    width_adjustments = [0, 0, 0, 5, 5, 5]
    x_offsets = [0, 0, 0, 3, 3, 3]

    problem_solve_draw(canvas_obj, drawer, problem_solve_score, rect_color_1,
                       base_positions[0], base_y,
                       width_adjust=width_adjustments[0],
                       x_offset=x_offsets[0])
    doubt_draw(canvas_obj, drawer, doubt_score, rect_color_2,
               base_positions[1], base_y,
               width_adjust=width_adjustments[1],
               x_offset=x_offsets[1])
    help_draw(canvas_obj, drawer, help_score, rect_color_3,
              base_positions[2], base_y,
              width_adjust=width_adjustments[2],
              x_offset=x_offsets[2])
    fantasy_draw(canvas_obj, drawer, fantasy_score, rect_color_4,
                 base_positions[3], base_y,
                 width_adjust=width_adjustments[3],
                 x_offset=x_offsets[3])
    escape_draw(canvas_obj, drawer, escape_score, rect_color_5,
                base_positions[4], base_y,
                width_adjust=width_adjustments[4],
                x_offset=x_offsets[4])
    rationalization_draw(canvas_obj, drawer, rationalization_score, rect_color_6,
                         base_positions[5], base_y,
                         width_adjust=width_adjustments[5],
                         x_offset=x_offsets[5])

# Helper function to draw page 15 horizontal lines
def draw_p15_lines(canvas_obj, start_x, start_y, line_length, count=6, labels=None):
    """Draw horizontal guidance lines for the page 15 competency graph."""
    canvas_obj.setStrokeColorRGB(p15_light_grey[0], p15_light_grey[1], p15_light_grey[2])
    canvas_obj.setLineWidth(0.3)
    if labels is None:
        labels = [counter * 20 for counter in range(count + 1)]

    for index, label in enumerate(labels):
        y_pos = start_y + (index * 35)
        canvas_obj.line(start_x, y_pos, start_x + line_length, y_pos)
        canvas_obj.setFont('FZLanTingXiHei', 12)
        canvas_obj.setFillColorRGB(0, 0, 0)
        canvas_obj.drawRightString(start_x - 10, y_pos, str(label))

# Define function to draw page 15 competency graph
def draw_p15_graph(canvas_obj, drawer, scores, colors, start_x, start_y):
    """
    Draw complete page 15 competency graph with 8 bar charts
    Parameters:
        canvas_obj: Canvas object
        drawer: PDFDrawer object
        scores: List of 8 scores
        colors: List of 8 colors
        start_x: Starting x position
        start_y: Starting y position
    """
    base_y = start_y
    spacing = 50 * 1.15  # Increase distance between rectangles by 15%

    # Draw guidance lines behind the bars
    line_length = spacing * (len(scores) - 1) + 80
    p15_labels = list(range(1, 16))
    draw_p15_lines(canvas_obj, start_x - 10, base_y, line_length,
                   count=len(p15_labels) - 1, labels=p15_labels)
    
    # Draw all 8 competency bars
    competency_draw_1(canvas_obj, drawer, scores[0], colors[0], start_x + (spacing * 0), base_y)
    competency_draw_2(canvas_obj, drawer, scores[1], colors[1], start_x + (spacing * 1), base_y)
    competency_draw_3(canvas_obj, drawer, scores[2], colors[2], start_x + (spacing * 2), base_y)
    competency_draw_4(canvas_obj, drawer, scores[3], colors[3], start_x + (spacing * 3), base_y)
    competency_draw_5(canvas_obj, drawer, scores[4], colors[4], start_x + (spacing * 4), base_y)
    competency_draw_6(canvas_obj, drawer, scores[5], colors[5], start_x + (spacing * 5), base_y)
    competency_draw_7(canvas_obj, drawer, scores[6], colors[6], start_x + (spacing * 6), base_y)
    competency_draw_8(canvas_obj, drawer, scores[7], colors[7], start_x + (spacing * 7), base_y)

# Define function to draw page 13 circular graph
def p13graph(canvas_obj, center_x, center_y, circle_degree_value, outer_diameter, inner_diameter,
             fill_color=deepblue, alpha=0.5):
    """Draw thick rounded arc for page 13."""
    radius_outer = outer_diameter / 2
    radius_inner = inner_diameter / 2
    thickness = radius_outer - radius_inner
    mid_radius = radius_inner + (thickness / 2)

    canvas_obj.saveState()
    canvas_obj.setLineWidth(thickness)
    canvas_obj.setLineCap(1)
    canvas_obj.setStrokeColorRGB(fill_color[0], fill_color[1], fill_color[2], alpha=alpha)
    canvas_obj.arc(center_x - mid_radius, center_y - mid_radius,
                   center_x + mid_radius, center_y + mid_radius,
                   0, circle_degree_value)
    canvas_obj.restoreState()


def draw_p11_graph(canvas_obj, center_x, center_y, circle_degree_value,
                   outer_diameter, inner_diameter, stroke_color, alpha=0.5):
    """Draw thick rounded arc for page 11."""
    radius_outer = outer_diameter / 2
    radius_inner = inner_diameter / 2
    thickness = radius_outer - radius_inner
    mid_radius = radius_inner + (thickness / 2)

    canvas_obj.saveState()
    canvas_obj.setLineWidth(thickness)
    canvas_obj.setLineCap(1)  # round caps to create semicircle ends
    canvas_obj.setStrokeColorRGB(stroke_color[0], stroke_color[1], stroke_color[2], alpha=alpha)
    canvas_obj.arc(center_x - mid_radius, center_y - mid_radius,
                   center_x + mid_radius, center_y + mid_radius,
                   0, circle_degree_value)
    canvas_obj.restoreState()
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


def draw_center_white_rect(drawer, center_x, center_y, width, height):
    """
    Draw a white rectangle centered at the specified position.
    Returns the bottom-left coordinates along with width and height.
    """
    bottom_left_x = center_x - (width / 2)
    bottom_left_y = center_y - (height / 2)
    draw_white_rectangle(drawer, bottom_left_x, bottom_left_y, width, height)
    return bottom_left_x, bottom_left_y, width, height

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


def draw_paragraph_in_rect(canvas_obj, text, x, y, width, height, style=None):
    """
    Draw a paragraph within a rectangle area.
    """
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT

    if style is None:
        default_style = ParagraphStyle(
            name="Page9Paragraph",
            parent=getSampleStyleSheet()['Normal'],
            fontName='FZLanTingXiHei',
            fontSize=12,
            leading=14,
            alignment=TA_LEFT,
            textColor=colors.black,
        )
    else:
        default_style = style

    paragraph = Paragraph(text, default_style)
    paragraph.wrapOn(canvas_obj, width, height)
    paragraph.drawOn(canvas_obj, x, y)

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
            image=f"pdf_generate_api/original_png/{image_name}",
            x=0,
            y=0,
            width=page_width,
            height=page_height
        )


# Initialize page number counter
page_counter = 1

# Create 16 pages WITHOUT ruler overlay
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
    
    # ============================================================
    # SECTION 1: PAGE 1 EDITS (page_number == 0)
    # ============================================================
    if page_number == 0:
        # No edits for page 1
        pass
    
    # ============================================================
    # SECTION 2: PAGE 2 EDITS (page_number == 1)
    # ============================================================
    if page_number == 1:
        # Draw full-width white rectangle at bottom
        draw_white_rectangle(drawer, x=0, y=50, width=page_width, height=200)
        
        # Draw white rectangle at specified position (increased width by 100, moved 50 to right)
        draw_white_rectangle(drawer, x=190, y=60, width=360, height=440)
        
        # Get canvas object for drawing text
        canvas_obj = pdf.get_canvas()

        # Draw personal information table
        info_table_data = {
            "name": student_name,
            "sex": student_sex,
            "birth_date": student_birth_date,
            "test_date": student_test_date,
            "age": student_age,
            "school": student_school,
            "phone": student_phone,
        }

        person_info_col_widths = [
            0.5 * cm,
            0.5 * cm,
            0.5 * cm,
            0.5 * cm,
            0.5 * cm,
            10 * cm,
        ]

        person_info_row_heights = [1 * cm] * 7

        drawer.draw_person_info_table(
            x=200,
            y=230,
            info=info_table_data,
            col_widths=person_info_col_widths,
            row_heights=person_info_row_heights,
            dotted_line_image="p3/dottedline.png",
        )
        
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
    
    # ============================================================
    # SECTION 3: PAGE 3 EDITS (page_number == 2)
    # ============================================================
    if page_number == 2:
        # Draw full-width white rectangle
        draw_white_rectangle(drawer, x=0, y=380, width=page_width, height=110)
        
        # Draw white rectangle at new position
        draw_white_rectangle(drawer, x=450, y=650, width=80, height=65)
        
        # Get canvas object for drawing
        canvas_obj = pdf.get_canvas()
        
        # Print resilience score (adjusted for new rectangle position)
        print_score(canvas_obj, resilience_score, 450 + 20 + 5, 650 + 65 + 10 - 60)
    
    # ============================================================
    # SECTION 4: PAGE 4 EDITS (page_number == 3)
    # ============================================================
    if page_number == 3:
        # No edits for page 4
        pass
    
    # ============================================================
    # SECTION 5: PAGE 5 EDITS (page_number == 4)
    # ============================================================
    if page_number == 4:
        # No edits for page 5
        pass
    
    # ============================================================
    # SECTION 6: PAGE 6 EDITS (page_number == 5)
    # ============================================================
    if page_number == 5:
        # No edits for page 6
        pass
    
    # ============================================================
    # SECTION 7: PAGE 7 EDITS (page_number == 6)
    # ============================================================
    if page_number == 6:
        # Draw white filled rectangle (no border) at center
        draw_white_rectangle(drawer, x=160, y=310, width=300, height=220)
        
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
            ('外倾性 E', E_score, 'center', vertices[0][0], vertices[0][1] + 20),  # Top (moved 5pts up)
            ('宜人性 A', A_score, 'left', vertices[4][0] - 10 - 20, vertices[4][1]),    # Top-left (moved 20pts left)
            ('开放性 O', O_score, 'left', vertices[1][0] - 5 + 20, vertices[1][1]),    # Top-right (moved 20pts right)
            ('尽责性 C', C_score, 'left', vertices[3][0] - 25, vertices[3][1] - 15),  # Bottom-left
            ('神经质 N', N_score, 'left', vertices[2][0] + 15, vertices[2][1] - 10)   # Bottom-right
        ]
        
        # Draw text labels and scores for each vertex using loop
        for text, score, alignment, x, y in text_data:
            draw_pentagon_text(canvas_obj, text, alignment, x, y)
            draw_pentagon_score_text(canvas_obj, score, alignment, x, y)
        
        # Find min and max scores from pentagon variables
        min_score, max_score = find_min_max_scores(E_score, A_score, C_score, N_score, O_score)
        
        # Print max_score in leftmost top right rectangle (moved 70pts lower total: 35+35)
        print_score(canvas_obj, max_score, 430 + 10, 650 + 60 + 20 - 35 - 35)
        
        # Print min_score (moved 70pts lower and additional 20pts to the right)
        print_score(canvas_obj, min_score, 430 + 10 + 25 + 20 + 20, 650 + 60 + 20 - 35 - 35)
    
    # ============================================================
    # SECTION 8: PAGE 8 EDITS (page_number == 7)
    # ============================================================
    if page_number == 7:
        # No edits for page 8
        pass
    
    # ============================================================
    # SECTION 9: PAGE 9 EDITS (page_number == 8)
    # ============================================================
    if page_number == 8:
        # Draw white rectangle at specified position for stress coping score
        # Width increased by 100% (40->80), moved 40pts right, moved 5pts lower
        stress_score_x = 450 + 40 + 30 - 40
        stress_score_y = 670 - 5
        draw_center_white_rect(
            drawer,
            center_x=stress_score_x,
            center_y=stress_score_y + (score_background_height / 2),
            width=score_background_width,
            height=score_background_height,
        )
        
        # Draw white rectangle for bar chart area
        draw_white_rectangle(drawer, x=60, y=280, width=470, height=230)
        
        # Get canvas object for drawing
        canvas_obj = pdf.get_canvas()
        
        # Print stress coping score (adjusted position for moved rectangle)
        print_score(canvas_obj, stress_coping_score, stress_score_x, stress_score_y)
        
        # Draw page 9 graph with orange lines and bar charts
        draw_p9_graph(canvas_obj, drawer, problem_solve_score, doubt_score, help_score,
                     fantasy_score, escape_score, rationalization_score,
                     rect_color_1, rect_color_2, rect_color_3, rect_color_4, rect_color_5, rect_color_6)
        
        # Draw two white rectangles at three different y positions
        page9_rects = []
        page9_rects.extend(draw_two_white_rect(drawer, 200))
        page9_rects.extend(draw_two_white_rect(drawer, 135))
        page9_rects.extend(draw_two_white_rect(drawer, 65, y_offset=5))

        page9_texts = [text_1, text_2, text_3, text_4, text_5, text_6]
        paragraph_style = ParagraphStyle(
            name="Page9ParagraphStyle",
            parent=getSampleStyleSheet()['Normal'],
            fontName='FZLanTingXiHei',
            fontSize=12,
            leading=14,
            alignment=TA_LEFT,
            textColor=colors.black,
        )

        for rect_info, paragraph_text in zip(page9_rects, page9_texts):
            x_pos, y_pos, rect_width, rect_height = rect_info
            draw_paragraph_in_rect(
                canvas_obj,
                paragraph_text,
                x_pos,
                y_pos,
                rect_width,
                rect_height,
                style=paragraph_style,
            )
    
    # ============================================================
    # SECTION 10: PAGE 10 EDITS (page_number == 9)
    # ============================================================
    if page_number == 9:
        # No edits for page 10
        pass
    
    # ============================================================
    # SECTION 11: PAGE 11 EDITS (page_number == 10)
    # ============================================================
    if page_number == 10:
        # Get canvas object for drawing
        canvas_obj = pdf.get_canvas()
        center_x = page_width / 2
        center_y = page_height / 2

        # Draw center white rectangle behind graph
        draw_center_white_rect(drawer, center_x, center_y, 160, 160)

        # Draw layered circular arcs using new helper with individual degrees
        draw_p11_graph(canvas_obj, center_x, center_y, attrativeness_score,
                       outer_diameter=110, inner_diameter=90,
                       stroke_color=p11_yellow, alpha=0.5)

        draw_p11_graph(canvas_obj, center_x, center_y, leadership_score,
                       outer_diameter=130, inner_diameter=110,
                       stroke_color=p11_light_blue, alpha=0.4)

        draw_p11_graph(canvas_obj, center_x, center_y, leadership_skill_score,
                       outer_diameter=160, inner_diameter=140,
                       stroke_color=p11_dark_blue, alpha=0.3)

        # Draw vertical grey line connecting arc starts
        canvas_obj.setStrokeColorRGB(vertical_grey[0], vertical_grey[1], vertical_grey[2])
        canvas_obj.setLineWidth(2)
        max_radius = 160 / 2
        x_line = center_x + max_radius
        canvas_obj.line(x_line, center_y - max_radius, x_line, center_y + max_radius)

        # Draw competency score with centered white rectangle background
        competency_score_x = 520
        competency_score_y = 680
        draw_center_white_rect(
            drawer,
            center_x=competency_score_x,
            center_y=competency_score_y + (score_background_height / 2),
            width=score_background_width,
            height=score_background_height,
        )
        print_score(canvas_obj, f"{competency_score:.2f}", competency_score_x, competency_score_y)
    
    # ============================================================
    # SECTION 12: PAGE 12 EDITS (page_number == 11)
    # ============================================================
    if page_number == 11:
        # No edits for page 12
        pass
    
    # ============================================================
    # SECTION 13: PAGE 13 EDITS (page_number == 12)
    # ============================================================
    if page_number == 12:
        # Get canvas object for drawing
        canvas_obj = pdf.get_canvas()
        center_x = page_width / 2
        center_y = page_height / 2

        # Increase graph size and draw centered white rectangle
        outer_diameter = 220
        inner_diameter = 180
        draw_center_white_rect(drawer, center_x, center_y, outer_diameter, outer_diameter)

        # Draw layered arcs for page 13 using helper function
        p13graph(canvas_obj, center_x, center_y, circle_degree, outer_diameter, inner_diameter,
                 fill_color=deepblue, alpha=0.5)

        # Draw filled grey circle inside smaller radius
        inner_radius = inner_diameter / 2
        canvas_obj.setFillColorRGB(0.7, 0.7, 0.7)
        canvas_obj.circle(center_x, center_y, inner_radius - 10, stroke=0, fill=1)

        # Draw technical score at circle center
        technical_score_text = f"{technical_score:.2f}"
        text_width = canvas_obj.stringWidth(technical_score_text, 'Impact', 40)
        print_score(canvas_obj, technical_score_text,
                    center_x - (text_width / 2),
                    center_y - 20)

        # Draw technical score card at top right similar to page 11
        technical_score_card_x = 520
        technical_score_card_y = 620
        draw_center_white_rect(
            drawer,
            center_x=technical_score_card_x,
            center_y=technical_score_card_y + (score_background_height / 2),
            width=score_background_width,
            height=score_background_height,
        )
        print_score(canvas_obj, technical_score_text, technical_score_card_x, technical_score_card_y)
    
    # ============================================================
    # SECTION 14: PAGE 14 EDITS (page_number == 13)
    # ============================================================
    if page_number == 13:
        # No edits for page 14
        pass
    
    # ============================================================
    # SECTION 15: PAGE 15 EDITS (page_number == 14)
    # ============================================================
    if page_number == 14:
        # Draw full-width white rectangle
        draw_white_rectangle(drawer, x=0, y=170, width=page_width, height=300)
        
        # Get canvas object for drawing
        canvas_obj = pdf.get_canvas()
        
        # Prepare scores and colors for page 15 graph
        p15_scores = [
            interpersonal_score, 
            customer_service_score, 
            achievement_score, 
            thinking_score,
            market_sensitivity_score, 
            teamwork_score, 
            knowledge_skill_score, 
            influence_score
        ]
        
        p15_colors = [
            comp_color_1, comp_color_2, comp_color_3, comp_color_4,
            comp_color_5, comp_color_6, comp_color_7, comp_color_8
        ]
        
        # Draw the competency graph at position (50, 170)
        draw_p15_graph(canvas_obj, drawer, p15_scores, p15_colors, 80, 170)

        # Draw communication scores with background rectangles
        communication_entries = [
            (460, 670, communication_score),
            (460, 600, communication_percentile),
        ]

        for entry_x, entry_y, entry_value in communication_entries:
            draw_center_white_rect(
                drawer,
                center_x=entry_x,
                center_y=entry_y + (score_background_height / 2),
                width=score_background_width,
                height=score_background_height,
            )
            print_score(canvas_obj, f"{entry_value:.2f}", entry_x, entry_y)
    
    # ============================================================
    # SECTION 16: PAGE 16 EDITS (page_number == 15)
    # ============================================================
    if page_number == 15:
        # No edits for page 16
        pass

    # ============================================================
    # RULER MODULE - Disabled for v4 output (no ruler overlay)
    # ============================================================

    # show_page() adds a new page to the PDF
    # We call this after each page except the last one
    if page_number < 15:  # If not the last page (pages 0-14)
        pdf.show_page()

# Save the PDF file
# This writes all the pages to the file on your computer
pdf.save()
print("PDF created successfully with 16 pages, A4 size, without ruler overlay!")

