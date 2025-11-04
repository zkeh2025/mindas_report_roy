# import library and package
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle


# register chinese font
pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
# create a page
filename = "reportlab_v1.pdf"
c = canvas.Canvas(filename)

# Roy's function library


def draw_string_vertically_centered(c, x, y, text, font='Helvetica', font_size=12, color=[0, 0, 0]):
    """
    绘制垂直居中的文本
    Args:
        c: Canvas对象
        x: X坐标（文本中心）
        y: Y坐标（文本中心）
        text: 文本内容
        font: 字体名称
        font_size: 字体大小
        color: 颜色 [r, g, b]
    """
    c.setFont(font, font_size)
    c.setFillColorRGB(color[0], color[1], color[2])
    # 估算文本高度（通常为字体大小的1.2倍）
    text_height = font_size * 1.2
    # 调整Y坐标，使定位点变为文本中心
    adjusted_y = y + (text_height / 2)
    c.drawString(x, adjusted_y, text)


def upload_image(c, image, x, y, width=None, height=None, mask=None):
    while True:
        if width is None or height is None:
            c.drawImage(
                image,
                x=x,
                y=y,
                width=None,
                height=None,
                preserveAspectRatio=True,
                mask=mask
            )
            break
        elif isinstance(width, (int, float)) or isinstance(height, (int, float)):
            c.drawImage(
                image,
                x=x,
                y=y,
                width=width,
                height=height,
                preserveAspectRatio=False,
                mask=mask
            )
            break
        else:
            raise ValueError("width and height must be None or float")


def draw_bulltin(
    evaluation_content: list = ["推理能力", "空间能力", "加工速度", "自我概念", "思维模式", "自驱力"],
    y_start: float = 160,
    x_start: float = 0,
    r: float = 5,
    x_cen: float = -12,
    y_decreament: float = 20,
    y_circle_start: float = 163,
    linewidth: float = 0.5,
    font_size: float = 23,
):
    for item in evaluation_content:
        # set up counter1 and counter2 with increment for position of bulltin
        y = y_start-(evaluation_content.index(item)*y_decreament)
        y_circle = y_circle_start-(evaluation_content.index(item)*y_decreament)

        c.setFont("STSong-Light", size=font_size)
        c.setFillColorRGB(0, 0, 0)
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(linewidth*mm)
        # rotate coordinate
        c.rotate(90)
        # draw eclipse
        c.circle(y_circle*mm, x_cen*mm, r*mm, stroke=1, fill=0)
        # drawstring number counter

        # rotate back
        c.rotate(-90)
        # draw number in circle
        c.setFont("STSong-Light", size=font_size)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x_start+10*mm, y*mm,
                     str(evaluation_content.index(item)+1))
        # draw string beside circle
        c.setFont("STSong-Light", size=font_size)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x_start+20*mm, y*mm, item)

        # add space between each list


def draw_line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    width: float = 1,
    color: list[float, float, float] = [0, 0, 0],
):
    c.setStrokeColorRGB(color[0], color[1], color[2])
    c.setLineWidth(width*mm)
    c.line(x1, y1, x2, y2)


def draw_string_list(
    x: float = 0, y: float = 0,
    r: float = 0.0, g: float = 0.0, b: float = 0.0,
    font: str = "Helvetica",
    font_size: float = 50,
    label_list: list[str] = [],
    colon: str = "",
    text_list: list[str] = ["B4"],
):
    for item in text_list:
        c.setFont(font, font_size)
        c.setFillColorRGB(r, g, b)
        if colon == ":":
            c.drawString(mm*x+10, mm*y+(text_list.index(item)+1)
                         * font_size, text=":")
        c.drawString(mm*x+10+20, mm*y+(text_list.index(item)+1)
                     * font_size, text=item)

    for item in label_list:
        c.drawString(mm*x, mm*y+(label_list.index(item)+1)
                     * font_size, text=item)


def draw_string(
    x: float = 0, y: float = 0,
    font: str = "Helvetica",
    font_size: float = 50,
    color: list[float, float, float] = [0, 0, 0],
    text: str = ["B4"],
):
    c.setFont(font, font_size)
    c.setFillColorRGB(color[0], color[1], color[2])
    c.drawString(x, y, text=text)


def draw_rect(
    pos_x: float = 0,
    pos_y: float = 0,
    width: float = 40,
    height: float = 40,
    radius: float = 5,
    color: list[float, float, float] = [0, 0, 0],
    stroke: bool = 0,
    fill: bool = 1,
):
    c.setFillColorRGB(color[0], color[1], color[2])
    c.roundRect(pos_x, pos_y, mm*width, mm*height, radius=mm*radius,
                stroke=stroke, fill=fill)


def draw_dotted_line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    width: float = 1,
    color: list[float, float, float] = [0, 0, 0],
    dash: list[float, float] = [2, 1],
    alpha: float = 1,
):
    c.setStrokeColorRGB(color[0], color[1], color[2], alpha=alpha)
    c.setLineWidth(width*mm)
    c.setDash(dash)
    c.line(x1, y1, x2, y2)


cyan = [0.17255,  0.67059,  0.69804]
darkercyan = [0.18824,  0.58431,  0.50588]
black = [0, 0, 0]
lightcyan = [0.18824,  0.58824,  0.50588]
red = [0.70980,  0.06275,  0.12941]
lightpurple = [0.66667, 0.69412, 0.83137]
orange = [1.00000, 0.63922,  0.00000]
darkblue = [0.02353, 0.14902,  0.30980]
green = [0.0, 0.8, 0.0]  # Green color for high score performance
white_color = [1, 1, 1]
# draw b4 rect
draw_rect(pos_x=62, pos_y=712, width=40,
          height=60, radius=5, color=darkercyan)

# B4 drawstring
draw_string(x=80, y=740, text="B4", color=black)
# b4 drawline
draw_line(155, 710, 595, 710, color=darkercyan)
draw_line(155, 799, 600, 799, color=darkercyan)

# draw in b4 line
upload_image(c, "shaonian.png", 225, 732, width=34, height=34)
upload_image(c, "perception.png", 225, 732, width=34, height=34)
# draw face
upload_image(c, "face.png", 220, 94, )
# draw 测评内容
draw_bulltin(
    y_start=150,
    x_start=20,
    r=3,
    x_cen=-18.5,
    y_decreament=20,
    y_circle_start=152,
    linewidth=0.5,
    font_size=17,)

# def paragraph_generate
style_sheet = getSampleStyleSheet()

top_style = ParagraphStyle(
    name="bottomstyle",
    parent=style_sheet['Normal'],
    alignment=TA_JUSTIFY,
    fontName="STSong-Light",
    fontSize=13,
    leading=10,
    textColor=cyan,
)


top_text = """<font size = 16><b>DAN成长计划</b></font><br/>
<font size=9>PSYCHDREAM YOUNG</font>"""

justifyparagraph = Paragraph(top_text, top_style)
justifyparagraph.wrapOn(c, 40*mm, 20*mm)
justifyparagraph.drawOn(c, 268, 740)

draw_line(387, 770, 387, 728, width=0.5,)
upload_image(c, "company_logo.png", 400, 732, width=34, height=34)

redstyle = ParagraphStyle(
    name="redstyle",
    parent=style_sheet['Normal'],
    alignment=TA_JUSTIFY,
    fontName="STSong-Light",
    fontSize=17,
    leading=10,
    textColor=red,
)
para = Paragraph(
    """双培强基工程<br/><font size=7> 青少年心里特色素质时间教育工程</font>""", redstyle)
para.wrapOn(c, 40*mm, 20*mm)
para.drawOn(c, 440, 740)

draw_string(60, 650, font="STSong-Light", font_size=25,
            color=lightcyan, text="分析型测评包")
draw_string(60, 600, font="STSong-Light", font_size=40,
            color=lightcyan, text="核心认知能力和")
draw_string(60, 550, font="STSong-Light", font_size=40,
            color=lightcyan, text="成长型思维")

draw_rect(60, 500, width=40, height=11,
          color=lightcyan, radius=1, fill=True)
draw_string(70, 510, font="STSong-Light",
            font_size=23, color=white_color, text="测评内容")

list_items = ["发", "现", "自", "己"]
x = 15

for item in list_items:
    i = (int(list_items.index(item)+1))
    draw_string(20+i*12*mm, 60, font="STSong-Light",
                font_size=x, color=black, text=item)

list_items2 = ["点", "亮", "未", "来"]
for item in list_items2:
    i = (int(list_items2.index(item)+1))
    draw_string(180+i*12*mm, 60, font="STSong-Light",
                font_size=x, color=black, text=item)

c.showPage()

upload_image(c, "company_logo.png", 5.82*cm,
             24.82*cm, width=70, height=70)

para = Paragraph(
    """双培强基工程<br/><font size=7> 青少年心里特色素质时间教育工程</font>""", redstyle)
para.wrapOn(c, 40*mm, 20*mm)
para.drawOn(c, 8.83*cm, 26*cm)

draw_dotted_line(3.42*cm, 23.5*cm, 16.42*cm, 23.5*cm,
                 width=0.5, dash=[4, 2], color=[0.8, 0.6, 0.9])
draw_dotted_line(3.42*cm, 14.5*cm, 16.42*cm, 14.5*cm,
                 width=0.5, dash=[4, 2], color=[0.8, 0.6, 0.9])

name = "张三"
sex = "男"
birth = "2000年1月1日"
testdate = "2023年12月1日"
grade = "10年级"
school = "中国高中"
phone = "12345678901"

table = Table(
    data=([
        ["姓", "", "", "名", "：", name],
        ["性", "", "", "别", "：", sex],
        ["出", "生", "日", "期", "：", birth],
        ["测", "试", "日", "期", "：", testdate],
        ["年", "", "", "级", "：", grade],
        ["学", "", "", "校", "：", school],
        ["联", "系", "电", "话", "：", phone],
    ]),
    colWidths=[0.5*cm, 0.5*cm, 0.5*cm, 0.5*cm, 0.5*cm, 10*cm],
    rowHeights=[1*cm]*7,
)

tablestyle = TableStyle([
    ('ALIGN', (0, 0), (4, 6), 'CENTER'),
    ('ALIGN', (6, 0), (5, 6), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, -1), 'STSong-Light'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
])

table.setStyle(tablestyle)
table.wrapOn(c, 0, 0)
table.drawOn(c, 3.42*cm, 15.76*cm)

teacher = "张三"
table = Table(
    data=([
        ["测", "评", "单", "位", "：", "双培强基工程·素质发展研究院"],
        ["测", "评", "老", "师", "：", teacher],

    ]),
    colWidths=[0.5*cm, 0.5*cm, 0.5*cm, 0.5*cm, 0.5*cm, 10*cm],
    rowHeights=[1*cm]*2,
)

tablestyle = TableStyle([
    ('ALIGN', (0, 0), (4, 1), 'CENTER'),
    ('ALIGN', (5, 0), (5, 1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, -1), 'STSong-Light'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
])

table.setStyle(tablestyle)
table.wrapOn(c, 0, 0)
table.drawOn(c, 3.42*cm, 11*cm)


def draw_cut_rectangle(
    c,
    x,
    y,
    height,
    width,
    corner,
):
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.5)

    p = c.beginPath()

    p.moveTo(x, y)
    p.lineTo(x, y+height-corner)
    p.lineTo(x+corner, y+height)
    p.lineTo(x+width, y+height)
    p.lineTo(x+width, y+corner)
    p.lineTo(x+width-corner, y)
    p.lineTo(x, y)

    c.drawPath(p, stroke=1, fill=0)


c.setDash()
draw_cut_rectangle(c, x=3.39*cm, y=6.9*cm, height=2.89 *
                   cm, width=14.21*cm, corner=0.6*cm)
c.setDash(4, 2)
draw_cut_rectangle(c, x=3.7*cm, y=7.2*cm, height=2.29 *
                   cm, width=13.61*cm, corner=0.6*cm)

draw_string(7.86*cm, 8.8*cm, font="STSong-Light", font_size=12, text="扫二维码")
draw_string(7.86*cm, 7.8*cm, font="STSong-Light",
            font_size=12, text="保存孩子电子报告   观看专家成长建议")

upload_image(c, "qrcode.png", 5.3*cm, 7.3*cm, width=2*cm, height=2*cm)


c.showPage()

draw_string(1.4*cm, 27.6*cm, font="STSong-Light",
            color=darkblue, font_size=17, text="认知能力测评报告")
draw_string(1.4*cm, 27*cm, font="Helvetica", color=darkblue,
            font_size=12, text="COGNITIVE ABILITY REPORT")

draw_line(1.3*cm, 23.7*cm, 19.7*cm, 23.7*cm,
          width=0.8, color=[0.9, 0.9, 0.9])


def draw_two_table(c, x, y):
    table = Table(
        data,
        colWidths=[0.3*cm, 0.3*cm, 0.3*cm, 0.3*cm, 0.3*cm, 10*cm],
        rowHeights=[0.6*cm]*2,
    )

    tablestyle = TableStyle([
        ('ALIGN', (0, 0), (4, 1), 'CENTER'),
        ('ALIGN', (5, 0), (5, 1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'STSong-Light'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ])

    table.setStyle(tablestyle)
    table.wrapOn(c, 0, 0)
    table.drawOn(c, x*cm, y*cm)


name = "张三"
birth = "2000年1月1日"
data = [
    ["姓", "", "", "名", "：", name],
    ["出", "生", "日", "期", "：", birth],
]
draw_two_table(c, 1.4, 25)

student_id = "M9822936"
teacherid = "DAN11352"

data = [
    ["档", "案", "I", "D", "：", student_id],
    ["指", "导", "", "师", "：", teacherid],
]
draw_two_table(c, 6.4, 25)


time = "2023年12月1日"
repcode = "123456789012345678"
data = [
    ["测", "试", "时", "间", "：", time],
    ["报", "告", "编", "码", "：", repcode],
]

draw_two_table(c, 11.4, 25)

upload_image(c, "company_logo.png", 16.8*cm,
             27.2*cm, width=30, height=30)

para = Paragraph(
    """<font size =11>双培强基工程</font><br/><font size=5> 青少年心里特色素质时间教育工程</font>""", redstyle)
para.wrapOn(c, 40*mm, 20*mm)
para.drawOn(c, 17.7*cm, 27.5*cm)

draw_string(17*cm, 26*cm, font="STSong-Light", font_size=10, text="电子报告")
draw_string(17*cm, 25.5*cm, font="STSong-Light", font_size=10, text="成长建议")

upload_image(c, "lightbulb.png", 1.3*cm, 21.5*cm, width=60, height=60)
draw_rect(pos_x=3.2*cm, pos_y=21.8*cm, width=1.3 *
          cm, height=0.3*cm, radius=2, color=orange)
x = 21.1
draw_string(3.7*cm, x*cm, font="STSong-Light",
            font_size=10, text="认知能力", color=[0, 0, 0])
draw_string(3.7*cm, x-1*cm, font="Helvetica", font_size=10,
            text="COGNITIVE ABILITY", color=darkblue)


blackstyle = ParagraphStyle(
    name="blackstyle",
    parent=style_sheet['Normal'],
    alignment=TA_JUSTIFY,
    fontName="STSong-Light",
    fontSize=9,
    leading=12,
    textColor=colors.black,
)

para = Paragraph("""认知能力是大脑加工、处理信息，认知客观事物内部逻辑，并运用知识、经验等解
决问题的能力。认知的过程包括感知、记忆、想象、思考、判断等。它被重视的原
因是人类所有的学习活动都离不开认知能力的运用。""", blackstyle)

para.wrapOn(c, 150*mm, 35*mm)
para.drawOn(c, 1.7*cm, 19.6*cm)

draw_line(1.3*cm, 16.7*cm, 19.7*cm, 26.7*cm,
          width=0.8, color=[0.9, 0.9, 0.9])


# function for different graphs
# different output for different data set
# look at pdf in a developer tool to see positin of line and string


# Page 4: Cognitive Ability Model Page
c.showPage()

# Page 4 Header
draw_string_vertically_centered(
    c, 1.4*cm, 27.6*cm, "认知能力模型", font="STSong-Light", font_size=17, color=darkblue)
draw_string_vertically_centered(
    c, 1.4*cm, 27*cm, "COGNITIVE ABILITY MODEL", font="Helvetica", font_size=12, color=darkblue)

# Personal Information Section (same as page 3)
name = "宫文学"
birth = "2008-01-08"
data = [
    ["姓", "", "", "名", "：", name],
    ["出", "生", "日", "期", "：", birth],
]
draw_two_table(c, 1.4, 25.5)

student_id = "M9822936"
teacherid = "DAN11352"
data = [
    ["档", "案", "I", "D", "：", student_id],
    ["指", "导", "", "师", "：", teacherid],
]
draw_two_table(c, 6.4, 25.5)

time = "2025-07-29"
repcode = "11340869020"
data = [
    ["测", "试", "时", "间", "：", time],
    ["报", "告", "编", "码", "：", repcode],
]
draw_two_table(c, 11.4, 25.5)

# Company logo and info (top right)
upload_image(c, "company_logo.png", 16.8*cm,
             27.2*cm, width=30, height=30)
para = Paragraph(
    """<font size =11>双培强基工程</font><br/><font size=5> 青少年心里特色素质时间教育工程</font>""", redstyle)
para.wrapOn(c, 40*mm, 20*mm)
para.drawOn(c, 17.7*cm, 27.5*cm)

draw_string(17*cm, 26*cm + (4*mm), font="STSong-Light",
            font_size=10, text="电子报告")
draw_string(17*cm, 25.5*cm + (4*mm), font="STSong-Light",
            font_size=10, text="成长建议")

# Gray line above DAN introduction text - moved up by 20mm
draw_line(1.3*cm, 23.2*cm + (20*mm), 19.7*cm, 23.2 *
          cm + (20*mm), width=0.8, color=[0.9, 0.9, 0.9])

# Introduction paragraph
intro_text = """DAN测评根据儿童青少年认知能力的发展重点，选取了感知觉、注意力、记忆力、推理能力、空间能力和信息加工速度六大指标作为对认知能力的综合评估。人与人之间，除整体认知能力的差异外，可能在各项子指标上也有所不同。每个人都有自己独有的优势和不足，以下是您在认知能力六项子指标上的得分情况："""

intro_style = ParagraphStyle(
    name="introstyle",
    parent=style_sheet['Normal'],
    alignment=TA_JUSTIFY,
    fontName="STSong-Light",
    fontSize=10,
    leading=14,
    textColor=colors.black,
)

intro_para = Paragraph(intro_text, intro_style)
intro_para.wrapOn(c, 150*mm, 40*mm)
intro_para.drawOn(c, 1.4*cm, 22.5*cm)


# Function to draw rounded rectangle with one rounded corner
def draw_rounded_rect_one_corner(c, x, y, width, height, corner_radius, stroke_color=[0, 0, 0], fill_color=None):
    """Draw a rectangle with only one rounded corner (top-right)"""
    c.setStrokeColorRGB(stroke_color[0], stroke_color[1], stroke_color[2])
    if fill_color:
        c.setFillColorRGB(fill_color[0], fill_color[1], fill_color[2])

    # Start path
    p = c.beginPath()

    # Move to bottom-left corner
    p.moveTo(x, y)

    # Draw to bottom-right corner
    p.lineTo(x + width - corner_radius, y)

    # Draw rounded corner (top-right)
    p.curveTo(x + width, y, x + width, y + corner_radius,
              x + width, y + corner_radius)

    # Draw to top-right corner
    p.lineTo(x + width, y + height)

    # Draw to top-left corner
    p.lineTo(x, y + height)

    # Draw back to start
    p.lineTo(x, y)

    if fill_color:
        c.drawPath(p, stroke=1, fill=1)
    else:
        c.drawPath(p, stroke=1, fill=0)


# Function to draw cognitive domain section in 2-column layout
def draw_cognitive_domain(c, x, y, chinese_name, english_name, description, percentile, is_left_column=True):
    # Calculate dimensions for 2-column layout
    if is_left_column:
        rect_x = (x-0.2)*cm
        rect_width = 7.5*cm
    else:
        rect_x = (x-0.2)*cm
        rect_width = 7.5*cm

    rect_y = (y-1.3)*cm
    # Increased height by 3mm + 3mm
    rect_height = 2.5*cm - (20*mm) + (3*mm) + (3*mm)
    # Increased width by 3mm + 3mm
    rect_width = 7.5*cm - (20*mm) + (3*mm) + (3*mm) - (1*cm)
    corner_radius = 0.45*cm  # Increased by 50% from 0.3cm

    # Draw rounded rectangle around each section
    draw_rounded_rect_one_corner(
        c, rect_x, rect_y, rect_width, rect_height, corner_radius, stroke_color=[0.6, 0.6, 0.6])

    # Draw Chinese title (vertically centered)
    chinese_x = rect_x + (2*mm)
    font_size = 12
    # More precise vertical centering calculation
    chinese_y = rect_y + (rect_height/2) - (font_size * 1.7 / 2)

    draw_string_vertically_centered(
        c, chinese_x, chinese_y, chinese_name, font="STSong-Light", font_size=font_size, color=darkblue)

    # Calculate Chinese title width and position English title after it
    c.setFont("STSong-Light", font_size)
    chinese_width = c.stringWidth(
        chinese_name, "STSong-Light", font_size)
    english_x = chinese_x + chinese_width + (3*mm)
    # More precise vertical centering calculation for English title
    english_font_size = 10
    english_y = rect_y + (rect_height/2) - (english_font_size * 1.7 / 2)

    draw_string_vertically_centered(
        c, english_x, english_y, english_name, font="Helvetica-Bold", font_size=10, color=darkblue)

    # Draw vertical grey line
    line_x = english_x - (1.5*mm)
    line_y_start = chinese_y + (font_size * 1.5) - (1*mm)
    line_y_end = chinese_y + (1*mm)

    draw_line(line_x, line_y_start, line_x, line_y_end,
              width=0.5, color=[0.6, 0.6, 0.6])

    # Draw rectangles with same colors as percentage.png
    # Regular rectangle: width=2cm, height=0.7cm
    rect1_x = rect_x + rect_width + (3*mm)
    rect1_y = rect_y + rect_height
    draw_rect(pos_x=rect1_x, pos_y=rect1_y, width=5*mm, height=2*mm, radius=0,
              color=darkblue, stroke=0, fill=1)

    # Rounded corner rectangle: width=5mm, height=5mm, with bottom-right corner rounded
    rect2_x = rect1_x  # Same x as rect1
    rect2_y = rect1_y - (5*mm*mm)  # rect2 top edge contacts rect1 bottom edge
    # Set line width to 0.1
    c.setLineWidth(0)
    draw_rounded_rect_one_corner(
        c, rect2_x, rect2_y, 5*mm*mm, 5*mm*mm, 1*mm, stroke_color=[0, 0, 0],
        fill_color=[0.7, 0.7, 0.7])

    # Draw description paragraph
    desc_x = chinese_x  # Aligned with Chinese title x
    desc_y = rect_y - (2*mm)  # 2mm above rectangle bottom

    # Create paragraph style for description
    desc_style = ParagraphStyle(
        name="descstyle",
        parent=style_sheet['Normal'],
        alignment=TA_JUSTIFY,
        fontName="STSong-Light",
        fontSize=9,
        leading=13,
        textColor=colors.black,
    )

    # Create and draw paragraph
    desc_para = Paragraph(description, desc_style)
    # Width: rect width minus margins, Height: 20mm
    desc_para.wrapOn(c, rect_width - (4*mm), 20*mm)
    # Draw from top to bottom by adjusting Y coordinate
    desc_para.drawOn(c, desc_x, desc_y - desc_para.height)


# Draw the six cognitive domains
cognitive_domains = [
    {
        "chinese": "感知觉",
        "english": "Perception",
        "description": "感知是认知、理解的基础。感知觉是大脑对作用于大脑的外部信息的整体看法和理解，整个加工过程包括获取信息、理解信息、选择信息和组织信息。",
        "percentile": "98"
    },
    {
        "chinese": "注意力",
        "english": "Attention",
        "description": "心理活动对一定对象的指向和集中。一般理解为对客观事物持续注意的能力，如做事专注，还是易分心。神经生理因、兴趣/动机、精神状态等均会影响一个人的注意力水平。",
        "percentile": "60"
    },
    {
        "chinese": "记忆力",
        "english": "Memory",
        "description": "记忆力是神经系统存储过往经验的能力，是学习的基础，一般包括识记、保持、再认和重现。记忆力的个体差异影响学习效率，如有的同学看3遍就记住了一个单词，而有的同学可能要7-8遍。",
        "percentile": "98"
    },
    {
        "chinese": "推理能力",
        "english": "Reasoning",
        "description": "推理能力是智力的核心成分，是一个人通过已有知识和经验，通过综合分析做出新判断的过程。推理能力的差异往往反应一个人洞悉事物本质，事物联系能力的高低。",
        "percentile": "86"
    },
    {
        "chinese": "空间能力",
        "english": "Spatial Ability",
        "description": "空间能力是大脑通过观察、触摸及想象对物体形状、位置判断的能力。它是大脑对外部信息的抽象表征和推理，是数学、自然科学、工程等重要学科领域用到的重要心理能力。",
        "percentile": "63"
    },
    {
        "chinese": "加工速度",
        "english": "Processing Speed",
        "description": "加工速度是大脑处理内部或外部信息的速度，和网速、手机使用流畅性一样，大脑的信息加工速度直接影响学习、思考和人际沟通的效率。",
        "percentile": "86"
    }
]

# Draw each cognitive domain in 2-column, 3-row layout filling bottom half of page
# Left column positions - moved +10mm on x-axis
left_x = 1.0 + (10*mm)/cm  # Convert 10mm to cm and add to original position
# Increased vertical spacing by another 5mm
left_y_positions = [22.0, 18.0, 14.0]

# Right column positions - moved +20mm on x-axis
right_x = 9.9 + (20*mm)/cm  # Convert 20mm to cm and add to original position
# Increased vertical spacing by another 5mm
right_y_positions = [22.0, 18.0, 14.0]

for i, domain in enumerate(cognitive_domains):
    if i < 3:  # First 3 domains go in left column
        x_pos = left_x
        y_pos = left_y_positions[i]
        is_left = True
    else:  # Last 3 domains go in right column
        x_pos = right_x
        y_pos = right_y_positions[i-3]
        is_left = False

    draw_cognitive_domain(
        c, x_pos, y_pos, domain["chinese"], domain["english"],
        domain["description"], domain["percentile"], is_left_column=is_left)

# Footer
draw_line(1.3*cm, 1.5*cm, 19.7*cm, 1.5*cm,
          width=0.8, color=[0.9, 0.9, 0.9])
draw_string(1.4*cm, 1.2*cm, font="STSong-Light", font_size=10, text="第 2 页")
draw_string(6*cm, 1.2*cm, font="STSong-Light", font_size=10,
            text="关注\"双培强基工程\"公众号，获取电子版报告和更多成长建议。")


# Create a new page (Page 5)
c.showPage()

# Page 5: Replicate B4 PDF page 5 content
# Page 5 Header
draw_string_vertically_centered(
    c, 1.4*cm, 27.6*cm, "成长性思维报告", font="STSong-Light", font_size=17, color=darkblue)
draw_string_vertically_centered(
    c, 1.4*cm, 27*cm, "GROWTH MINDSET REPORT", font="Helvetica", font_size=12, color=darkblue)

# Personal Information Section (same as previous pages)
name = "宫文学"
birth = "2008-01-08"
data = [
    ["姓", "", "", "名", "：", name],
    ["出", "生", "日", "期", "：", birth],
]
draw_two_table(c, 1.4, 25.5)

student_id = "M9822936"
teacherid = "DAN11352"
data = [
    ["档", "案", "I", "D", "：", student_id],
    ["指", "导", "", "师", "：", teacherid],
]
draw_two_table(c, 6.4, 25.5)

time = "2025-07-29"
repcode = "11340869020"
data = [
    ["测", "试", "时", "间", "：", time],
    ["报", "告", "编", "码", "：", repcode],
]

draw_two_table(c, 11.4, 25.5)

# Company logo and info (top right)
upload_image(c, "company_logo.png", 16.8*cm, 27.2*cm, width=30, height=30)
para = Paragraph(
    """<font size =11>双培强基工程</font><br/><font size=5> 青少年心里特色素质时间教育工程</font>""", redstyle)
para.wrapOn(c, 40*mm, 20*mm)
para.drawOn(c, 17.7*cm, 27.5*cm)

draw_string(17*cm, 26*cm + (4*mm), font="STSong-Light",
            font_size=10, text="电子报告")
draw_string(17*cm, 25.5*cm + (4*mm), font="STSong-Light",
            font_size=10, text="成长建议")

# Gray line above content
gray_line_x1 = 1.3*cm
gray_line_x2 = 19.7*cm
gray_line_y = 23.2*cm + (20*mm)
draw_line(gray_line_x1, gray_line_y, gray_line_x2,
          gray_line_y, width=0.8, color=[0.9, 0.9, 0.9])

# Introduction paragraph about growth mindset
intro_text = """成长性思维是指个体相信自己的能力可以通过努力、学习和坚持而得到发展的信念。与固定性思维不同，成长性思维认为智力、才能和能力都是可以培养和提升的。这种思维方式对个人的学习、发展和成功具有重要影响。"""

intro_style = ParagraphStyle(
    name="introstyle",
    parent=style_sheet['Normal'],
    alignment=TA_JUSTIFY,
    fontName="STSong-Light",
    fontSize=10,
    leading=14,
    textColor=colors.black,
)

intro_para = Paragraph(intro_text, intro_style)
intro_para.wrapOn(c, 150*mm, 40*mm)
intro_para.drawOn(c, 1.4*cm, 22.5*cm)

# Growth Mindset Characteristics Section
# Title
draw_string(1.4*cm, 20*cm, font="STSong-Light", font_size=14,
            color=darkblue, text="成长性思维特征")

# Characteristics list
characteristics = [
    "• 相信能力可以通过努力提升",
    "• 面对挑战时保持积极态度",
    "• 从失败中学习和成长",
    "• 重视过程而非只看结果",
    "• 愿意接受反馈和建议",
    "• 持续学习和自我改进"
]

char_y = 19*cm
for char in characteristics:
    draw_string(1.4*cm, char_y, font="STSong-Light", font_size=11,
                color=black, text=char)
    char_y -= 0.5*cm

# Development Suggestions Section
draw_string(1.4*cm, 15*cm, font="STSong-Light", font_size=14,
            color=darkblue, text="发展建议")

suggestions_text = """1. 培养"努力导向"的思维方式，关注学习过程而非结果
2. 学会从错误中学习，将失败视为成长的机会
3. 设定具有挑战性的目标，逐步提升自己的能力
4. 寻求和接受建设性的反馈，持续改进
5. 培养自我反思的习惯，定期评估自己的进步
6. 保持开放的心态，愿意尝试新的学习方法和策略"""

suggestions_style = ParagraphStyle(
    name="suggestionsstyle",
    parent=style_sheet['Normal'],
    alignment=TA_JUSTIFY,
    fontName="STSong-Light",
    fontSize=10,
    leading=14,
    textColor=colors.black,
)

suggestions_para = Paragraph(suggestions_text, suggestions_style)
suggestions_para.wrapOn(c, 150*mm, 60*mm)
suggestions_para.drawOn(c, 1.4*cm, 13*cm)

# Footer
draw_line(1.3*cm, 1.5*cm, 19.7*cm, 1.5*cm, width=0.8, color=[0.9, 0.9, 0.9])
draw_string(1.4*cm, 1.2*cm, font="STSong-Light", font_size=10, text="第 5 页")
draw_string(6*cm, 1.2*cm, font="STSong-Light", font_size=10,
            text="关注\"双培强基工程\"公众号，获取电子版报告和更多成长建议。")

c.save()
print(f"PDF created successfully: {filename}")
