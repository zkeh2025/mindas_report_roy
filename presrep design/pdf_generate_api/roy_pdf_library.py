# Roy's PDF Library
# 自定义PDF生成库，包含所有绘图和文本处理函数

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

# 注册中文字体
pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))


class Colors:
    """预定义颜色常量"""
    CYAN = [0.17255, 0.67059, 0.69804]
    DARKER_CYAN = [0.18824, 0.58431, 0.50588]
    BLACK = [0, 0, 0]
    LIGHT_CYAN = [0.18824, 0.58824, 0.50588]
    RED = [0.70980, 0.06275, 0.12941]
    LIGHT_PURPLE = [0.66667, 0.69412, 0.83137]
    ORANGE = [1.00000, 0.63922, 0.00000]
    DARK_BLUE = [0.02353, 0.14902, 0.30980]
    GREEN = [0.0, 0.8, 0.0]
    WHITE = [1, 1, 1]


class PDFDrawer:
    """PDF绘图工具类"""

    def __init__(self, canvas_obj):
        self.c = canvas_obj

    def draw_string_vertically_centered(self, x, y, text, font='Helvetica',
                                        font_size=12, color=None, alpha=1):
        """绘制垂直居中的文本"""
        if color is None:
            color = [0, 0, 0]
        self.c.setFont(font, font_size)
        self.c.setFillColorRGB(color[0], color[1], color[2], alpha=alpha)
        text_height = font_size * 1.2
        adjusted_y = y + (text_height / 2)
        self.c.drawString(x, adjusted_y, text)

    def upload_image(self, image, x, y, width=None, height=None, mask=None):
        """上传并绘制图像"""
        while True:
            if width is None or height is None:
                self.c.drawImage(image, x=x, y=y, width=None, height=None,
                                 preserveAspectRatio=True, mask=mask)
                break
            elif (isinstance(width, (int, float)) or
                  isinstance(height, (int, float))):
                self.c.drawImage(image, x=x, y=y, width=width, height=height,
                                 preserveAspectRatio=False, mask=mask)
                break
            else:
                raise ValueError("width and height must be None or float")

    def draw_bulletin(self, evaluation_content=None, y_start=160,
                      x_start=0, r=5, x_cen=-12, y_decrement=20,
                      y_circle_start=163, linewidth=0.5, font_size=23):
        """绘制项目符号列表"""
        if evaluation_content is None:
            evaluation_content = ["推理能力", "空间能力", "加工速度",
                                  "自我概念", "思维模式", "自驱力"]

        for item in evaluation_content:
            item_index = evaluation_content.index(item)
            y = y_start - (item_index * y_decrement)
            y_circle = y_circle_start - (item_index * y_decrement)

            self.c.setFont("STSong-Light", size=font_size)
            self.c.setFillColorRGB(0, 0, 0)
            self.c.setStrokeColorRGB(0, 0, 0)
            self.c.setLineWidth(linewidth)
            self.c.rotate(90)
            self.c.circle(y_circle, x_cen, r, stroke=1, fill=0)
            self.c.rotate(-90)
            self.c.setFont("STSong-Light", size=font_size)
            self.c.setFillColorRGB(0, 0, 0)
            self.c.drawString(x_start + 10, y, str(item_index + 1))
            self.c.setFont("STSong-Light", size=font_size)
            self.c.setFillColorRGB(0, 0, 0)
            self.c.drawString(x_start + 20, y, item)

    def draw_line(self, x1, y1, x2, y2, width=1, color=None, alpha=1,
                  dash=None):
        """绘制直线"""
        if color is None:
            color = [0, 0, 0]
        self.c.setStrokeColorRGB(color[0], color[1], color[2], alpha=alpha)
        self.c.setLineWidth(width)
        if dash is not None:
            self.c.setDash(dash)
        self.c.line(x1, y1, x2, y2)
        if dash is not None:
            self.c.setDash([])  # 重置虚线样式

    def draw_string_list(self, x=0, y=0, r=0.0, g=0.0, b=0.0,
                         font="Helvetica", font_size=50,
                         label_list=None, colon="", text_list=None):
        """绘制字符串列表"""
        if label_list is None:
            label_list = []
        if text_list is None:
            text_list = ["B4"]

        for item in text_list:
            self.c.setFont(font, font_size)
            self.c.setFillColorRGB(r, g, b)
            if colon == ":":
                self.c.drawString(x + 10,
                                  y + (text_list.index(item) +
                                       1) * font_size,
                                  text=":")
            self.c.drawString(x + 10 + 20,
                              y + (text_list.index(item) + 1) * font_size,
                              text=item)

        for item in label_list:
            self.c.drawString(x,
                              y + (label_list.index(item) + 1) *
                              font_size,
                              text=item)

    def draw_string(self, x=0, y=0, font="Helvetica", font_size=50,
                    color=None, text="B4", alpha=1):
        """绘制字符串"""
        if color is None:
            color = [0, 0, 0]
        self.c.setFont(font, font_size)
        self.c.setFillColorRGB(color[0], color[1], color[2], alpha=alpha)
        self.c.drawString(x, y, text=text)

    def draw_rect(self, pos_x=0, pos_y=0, width=40, height=40,
                  radius=0, color=None, stroke=0, fill=1, alpha=1,
                  borderalpha=1):
        """绘制矩形"""
        if color is None:
            color = [0, 0, 0]
        self.c.setFillColorRGB(color[0], color[1], color[2], alpha=alpha)
        self.c.setStrokeColorRGB(
            color[0], color[1], color[2], alpha=borderalpha)
        self.c.roundRect(pos_x, pos_y, width, height,
                         radius=radius, stroke=stroke, fill=fill)

    def draw_circle(self, x, y, radius, color=None, stroke=1, fill=0,
                    line_width=1, alpha=1):
        """绘制圆圈"""
        if color is None:
            color = [0, 0, 0]
        self.c.setStrokeColorRGB(color[0], color[1], color[2], alpha=alpha)
        self.c.setFillColorRGB(color[0], color[1], color[2], alpha=alpha)
        self.c.setLineWidth(line_width)
        self.c.circle(x, y, radius, stroke=stroke, fill=fill)

    def draw_dotted_line(self, x1, y1, x2, y2, width=1,
                         color=None, dash=None, alpha=1):
        """绘制虚线"""
        if color is None:
            color = [0, 0, 0]
        if dash is None:
            dash = [2, 1]
        self.c.setStrokeColorRGB(color[0], color[1], color[2], alpha=alpha)
        self.c.setLineWidth(width)
        self.c.setDash(dash)
        self.c.line(x1, y1, x2, y2)

    def draw_cut_rectangle(self, x, y, height, width, corner, alpha=1):
        """绘制切角矩形"""
        self.c.setStrokeColorRGB(0, 0, 0, alpha=alpha)
        self.c.setLineWidth(0.5)
        p = self.c.beginPath()
        p.moveTo(x, y)
        p.lineTo(x, y + height - corner)
        p.lineTo(x + corner, y + height)
        p.lineTo(x + width, y + height)
        p.lineTo(x + width, y + corner)
        p.lineTo(x + width - corner, y)
        p.lineTo(x, y)
        self.c.drawPath(p, stroke=1, fill=0)

    def draw_rounded_rect_one_corner(self, x, y, width, height,
                                     corner_radius, stroke_color=None,
                                     fill_color=None, alpha=1):
        """绘制只有一个圆角的矩形（右上角）"""
        if stroke_color is None:
            stroke_color = [0, 0, 0]
        self.c.setStrokeColorRGB(stroke_color[0], stroke_color[1],
                                 stroke_color[2], alpha=alpha)
        if fill_color:
            self.c.setFillColorRGB(fill_color[0], fill_color[1],
                                   fill_color[2], alpha=alpha)

        p = self.c.beginPath()
        p.moveTo(x, y)
        p.lineTo(x + width - corner_radius, y)
        p.curveTo(x + width, y, x + width, y + corner_radius,
                  x + width, y + corner_radius)
        p.lineTo(x + width, y + height)
        p.lineTo(x, y + height)
        p.lineTo(x, y)

        if fill_color:
            self.c.drawPath(p, stroke=1, fill=1)
        else:
            self.c.drawPath(p, stroke=1, fill=0)

    def draw_cognitive_domain(self, x, y, chinese_name, english_name,
                              description, percentile, is_left_column=True):
        """绘制认知领域部分（2列布局）"""
        # percentile参数暂时未使用，但保留以保持API兼容性
        _ = percentile

        if is_left_column:
            rect_x = x - 0.2
            rect_width = 7.5
        else:
            rect_x = x - 0.2
            rect_width = 7.5

        rect_y = y - 1.3
        rect_height = 2.5 - 20 + 3 + 3
        rect_width = 7.5 - 20 + 3 + 3 - 1
        corner_radius = 0.45

        self.draw_rounded_rect_one_corner(
            rect_x, rect_y, rect_width, rect_height, corner_radius,
            stroke_color=[0.6, 0.6, 0.6])

        chinese_x = rect_x + 2
        font_size = 12
        chinese_y = rect_y + (rect_height / 2) - (font_size * 1.7 / 2)

        self.draw_string_vertically_centered(
            chinese_x, chinese_y, chinese_name, font="STSong-Light",
            font_size=font_size, color=Colors.DARK_BLUE)

        self.c.setFont("STSong-Light", font_size)
        chinese_width = self.c.stringWidth(chinese_name, "STSong-Light",
                                           font_size)
        english_x = chinese_x + chinese_width + 3
        english_font_size = 10
        english_y = rect_y + (rect_height / 2) - (english_font_size * 1.7 / 2)

        self.draw_string_vertically_centered(
            english_x, english_y, english_name, font="Helvetica-Bold",
            font_size=10, color=Colors.DARK_BLUE)

        line_x = english_x - 1.5
        line_y_start = chinese_y + (font_size * 1.5) - 1
        line_y_end = chinese_y + 1

        self.draw_line(line_x, line_y_start, line_x, line_y_end,
                       width=0.5, color=[0.6, 0.6, 0.6], alpha=1)

        rect1_x = rect_x + rect_width + 3
        rect1_y = rect_y + rect_height
        self.draw_rect(pos_x=rect1_x, pos_y=rect1_y, width=5,
                       height=2, radius=0, color=Colors.DARK_BLUE,
                       stroke=0, fill=1)

        rect2_x = rect1_x
        rect2_y = rect1_y - (5)
        self.c.setLineWidth(0)
        self.draw_rounded_rect_one_corner(
            rect2_x, rect2_y, 5, 5, 1,
            stroke_color=[0, 0, 0], fill_color=[0.7, 0.7, 0.7])

        desc_x = chinese_x
        desc_y = rect_y - 2

        style_sheet = getSampleStyleSheet()
        desc_style = ParagraphStyle(
            name="descstyle",
            parent=style_sheet['Normal'],
            alignment=TA_JUSTIFY,
            fontName="STSong-Light",
            fontSize=9,
            leading=13,
            textColor=colors.black,
        )

        desc_para = Paragraph(description, desc_style)
        desc_para.wrapOn(self.c, rect_width - 4, 20)
        desc_para.drawOn(self.c, desc_x, desc_y - desc_para.height)

    def draw_two_table(self, x, y, data):
        """绘制两列表格"""
        table = Table(
            data,
            colWidths=[0.3, 0.3, 0.3, 0.3, 0.3, 10],
            rowHeights=[0.6] * 2,
        )

        tablestyle = TableStyle([
            ('ALIGN', (0, 0), (4, 1), 'CENTER'),
            ('ALIGN', (5, 0), (5, 1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'STSong-Light'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ])

        table.setStyle(tablestyle)
        table.wrapOn(self.c, 0, 0)
        table.drawOn(self.c, x, y)

    def draw_ruler(self, page_width, page_height):
        """在页面边缘绘制标尺"""
        # Calculate center positions for labels
        # Center X position (middle of page width)
        center_x = page_width / 2
        # Center Y position (middle of page height)
        center_y = page_height / 2

        # X轴标尺（覆盖整个页面宽度）
        for x in range(0, int(page_width), 10):  # 每10个单位一个刻度
            x_pos = x

            # 绘制垂直刻度线覆盖整个页面高度
            # All lines have the same width and alpha
            self.draw_line(x_pos, 0, x_pos, page_height,
                           width=0.5, color=Colors.BLACK, alpha=0.3)

            # 绘制数字标签 at middle of page (center_y) instead of edge
            # Place label at the vertical center of the page
            # Every other number (at x=10, 30, 50...) is offset by -10 pts
            # Check if this is an alternate number by seeing if x/10 is odd
            if (x % 20) == 10:
                # This is an alternate number (10, 30, 50, 70, etc.)
                label_y = center_y - 10
            else:
                # This is a regular number (0, 20, 40, 60, etc.)
                label_y = center_y

            # Font size is 8 points
            self.draw_string(x_pos + 1, label_y, text=str(x),
                             font_size=8, color=Colors.BLACK)

        # Y轴标尺（覆盖整个页面高度）
        for y in range(0, int(page_height), 10):  # 每10个单位一个刻度
            y_pos = y

            # 绘制水平刻度线覆盖整个页面宽度
            # All lines have the same width and alpha
            self.draw_line(0, y_pos, page_width, y_pos,
                           width=0.5, color=Colors.BLACK, alpha=0.3)

            # 绘制数字标签 at middle of page (center_x) instead of edge
            # Place label at the horizontal center of the page
            # Font size is 8 points
            self.draw_string(center_x, y_pos + 1, text=str(y),
                             font_size=8, color=Colors.BLACK)


class PDFGenerator:
    """PDF生成器主类"""

    def __init__(self, filename="output.pdf", pagesize=None):
        self.filename = filename
        if pagesize is not None:
            self.c = canvas.Canvas(filename, pagesize=pagesize)
        else:
            self.c = canvas.Canvas(filename)
        self.drawer = PDFDrawer(self.c)

    def save(self):
        """保存PDF文件"""
        self.c.save()
        print(f"PDF创建成功: {self.filename}")

    def show_page(self):
        """显示新页面"""
        self.c.showPage()

    def get_canvas(self):
        """获取Canvas对象"""
        return self.c

    def get_drawer(self):
        """获取绘图器对象"""
        return self.drawer


def create_pdf(filename="output.pdf", pagesize=None):
    """快速创建PDF生成器"""
    return PDFGenerator(filename, pagesize)


if __name__ == "__main__":
    # 创建PDF生成器
    pdf = create_pdf("example.pdf")
    drawer = pdf.get_drawer()

    # 绘制一些示例内容
    drawer.draw_string(100, 700, text="Hello World!", font_size=20)
    drawer.draw_rect(50, 600, width=100, height=50, color=Colors.CYAN)
    drawer.draw_line(50, 500, 200, 500, width=2, color=Colors.RED, alpha=1)

    # 保存PDF
    pdf.save()
