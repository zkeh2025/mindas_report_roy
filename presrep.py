# 导入 Roy PDF Library
from roy_pdf_library import PDFGenerator, PDFDrawer, Colors, create_pdf
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors


def draw_ruler(drawer, page_width, page_height):
    """在页面边缘绘制点标尺"""

    # X轴标尺（覆盖整个页面宽度）
    for x in range(0, int(page_width), 20):  # 每20pts一个刻度
        x_pos = x
        # 绘制垂直刻度线覆盖整个页面高度
        drawer.draw_line(x_pos, 0, x_pos, page_height,
                         width=0.25, color=Colors.BLACK, alpha=0.3)
        # 绘制数字标签
        drawer.draw_string(x_pos + 1, 1, text=str(x),
                           font_size=8, color=Colors.BLACK)

    # Y轴标尺（覆盖整个页面高度）
    for y in range(0, int(page_height), 20):  # 每20pts一个刻度
        y_pos = y
        # 绘制水平刻度线覆盖整个页面宽度
        drawer.draw_line(0, y_pos, page_width, y_pos,
                         width=0.25, color=Colors.BLACK, alpha=0.3)
        # 绘制数字标签
        drawer.draw_string(1, y_pos + 1, text=str(y),
                           font_size=8, color=Colors.BLACK)


def draw_blue_lines(drawer, page_width, y_position, length=70):
    """绘制蓝色装饰线"""
    center_x = page_width / 2  # 页面中心
    y_pos = y_position * mm

    # 绘制左线
    drawer.draw_line(
        x1=center_x - length * mm,
        y1=y_pos,
        x2=center_x,
        y2=y_pos,
        width=1,
        color=Colors.DARK_BLUE,
        dash=[4, 2]
    )

    # 绘制右线
    drawer.draw_line(
        x1=center_x,
        y1=y_pos,
        x2=center_x + length * mm,
        y2=y_pos,
        width=1,
        color=Colors.DARK_BLUE,
        dash=[4, 2]
    )


# 创建PDF并添加新页面
if __name__ == "__main__":
    # 页面尺寸（595 x 960 pts）
    custom_pagesize = (595, 960)

    # 创建PDF生成器
    pdf = create_pdf("presrep_output.pdf", pagesize=custom_pagesize)
    drawer = pdf.get_drawer()

    # 页面尺寸（595 x 960 pts）
    page_width = 595  # 宽度（pts）
    page_height = 960   # 高度（pts）

    # 绘制标尺
    draw_ruler(drawer, page_width, page_height)

    # 在指定位置绘制深蓝色矩形
    # x = 10mm, y = 235mm
    drawer.draw_rect(
        pos_x=10 * mm,
        pos_y=235 * mm,
        width=40 * mm,  # 宽度35mm
        height=45 * mm,  # 高度45mm
        color=Colors.DARK_BLUE,
        stroke=1,  # 描边
        fill=1     # 填充
    )

    # 绘制深蓝色直线从 (50,235) 到 (205,235)
    drawer.draw_line(
        x1=50 * mm,
        y1=235 * mm,
        x2=205 * mm,
        y2=235 * mm,
        width=2,
        color=Colors.DARK_BLUE
    )

    # 绘制深蓝色直线从 (50,280) 到 (205,280)
    drawer.draw_line(
        x1=50 * mm,
        y1=280 * mm,
        x2=205 * mm,
        y2=280 * mm,
        width=2,
        color=Colors.DARK_BLUE
    )

    # 添加文本"职工抗压和"
    drawer.draw_string(
        x=60 * mm,
        y=260 * mm,
        text="职工抗压和",
        font="STSong-Light",
        font_size=50,
        color=Colors.DARK_BLUE
    )

    # 添加文本"岗位胜任力"
    drawer.draw_string(
        x=60 * mm,
        y=240 * mm,
        text="岗位胜任力",
        font="STSong-Light",
        font_size=50,
        color=Colors.DARK_BLUE
    )

    # 添加新矩形
    drawer.draw_rect(
        pos_x=10 * mm,
        pos_y=195 * mm,
        width=80 * mm,
        height=20 * mm,
        color=Colors.DARK_BLUE,
        stroke=1,
        fill=1
    )

    # 添加文本"报告"
    drawer.draw_string(
        x=15 * mm,
        y=260 * mm,
        text="报告",
        font="STSong-Light",
        font_size=25,
        color=Colors.WHITE
    )

    # 添加文本"Report"
    drawer.draw_string(
        x=15 * mm,
        y=245 * mm,
        text="Report",
        font="Helvetica",
        font_size=25,
        color=Colors.WHITE
    )

    # 添加文本"测评内容"
    drawer.draw_string(
        x=20 * mm,
        y=205 * mm,
        text="测评内容",
        font="STSong-Light",
        font_size=23,
        color=Colors.WHITE
    )

    # 添加文本"Assessment Modules"
    drawer.draw_string(
        x=20 * mm,
        y=197 * mm,
        text="Assessment Modules",
        font="Helvetica",
        font_size=18,
        color=Colors.WHITE
    )

    # 绘制三个圆圈
    drawer.draw_circle(
        x=15 * mm,
        y=175 * mm,
        radius=3 * mm,
        color=Colors.BLACK,
        stroke=1,
        fill=0,
        line_width=2
    )

    drawer.draw_circle(
        x=15 * mm,
        y=160 * mm,
        radius=3 * mm,
        color=Colors.BLACK,
        stroke=1,
        fill=0,
        line_width=2
    )

    drawer.draw_circle(
        x=15 * mm,
        y=145 * mm,
        radius=3 * mm,
        color=Colors.BLACK,
        stroke=1,
        fill=0,
        line_width=2
    )

    # 在圆圈中心添加数字
    drawer.draw_string(
        x=14 * mm,
        y=174 * mm,
        text="1",
        font="Helvetica",
        font_size=12,
        color=Colors.BLACK
    )

    drawer.draw_string(
        x=14 * mm,
        y=159 * mm,
        text="2",
        font="Helvetica",
        font_size=12,
        color=Colors.BLACK
    )

    drawer.draw_string(
        x=14 * mm,
        y=144 * mm,
        text="3",
        font="Helvetica",
        font_size=12,
        color=Colors.BLACK
    )

    # 在圆圈右侧添加文本
    drawer.draw_string(
        x=20 * mm,
        y=172 * mm,
        text="基础心理特质（大五人格）",
        font="STSong-Light",
        font_size=25,
        color=Colors.BLACK
    )

    # 添加第二个文本
    drawer.draw_string(
        x=20 * mm,
        y=157 * mm,
        text="压力应对能力（心理韧性/应对方式）",
        font="STSong-Light",
        font_size=25,
        color=Colors.BLACK
    )

    # 添加第三个文本
    drawer.draw_string(
        x=20 * mm,
        y=142 * mm,
        text="岗位核心能力（通用/管理/技术/销售）",
        font="STSong-Light",
        font_size=25,
        color=Colors.BLACK
    )

    # 上传并绘制图像
    drawer.upload_image(
        image="profession.png",
        x=0 * mm,
        y=0 * mm,
        width=205 * mm,
        height=130 * mm
    )

    # 创建新页面
    pdf.show_page()

    # 在第二页也绘制标尺
    draw_ruler(drawer, page_width, page_height)

    # 在第二页添加居中标题
    canvas = pdf.get_canvas()
    canvas.setFont("STSong-Light", 30)
    canvas.setFillColorRGB(0, 0, 0)

    # 计算文本宽度并居中绘制
    text1 = "职工抗压和岗位胜任力测试"
    text_width1 = canvas.stringWidth(text1, "STSong-Light", 30)
    canvas.drawString((210 * mm - text_width1) / 2, 305 * mm, text1)

    # 添加"报告"文本
    text2 = "报告"
    text_width2 = canvas.stringWidth(text2, "STSong-Light", 30)
    canvas.drawString((210 * mm - text_width2) / 2, 273 * mm, text2)

    # 调用蓝色线条函数
    draw_blue_lines(drawer, page_width, 340)
    draw_blue_lines(drawer, page_width, 265)

    # 创建第三页
    pdf.show_page()

    # 在第三页也绘制标尺
    draw_ruler(drawer, page_width, page_height)

    # 在第三页添加文本"心理韧性测评报告"
    drawer.draw_string(
        x=30,
        y=880,
        text="心理韧性测评报告",
        font="STSong-Light",
        font_size=25,
        color=Colors.DARK_BLUE
    )

    # 在第三页添加文本"GENERAL ABILITY REPORT"
    drawer.draw_string(
        x=30,
        y=860,
        text="GENERAL ABILITY REPORT",
        font="Helvetica",
        font_size=15,
        color=Colors.DARK_BLUE
    )

    # 在第三页添加空的2列2行表格
    name = 123
    date = 123
    empty_table_data = [
        ["姓", "", "", "名", "：", name],
        ["出", "生", "日", "期", "：", date]
    ]

    from reportlab.platypus import Table, TableStyle
    table = Table(
        empty_table_data,
        colWidths=[5*mm, 5*mm, 5*mm, 5*mm, 5*mm, 40*mm],
        rowHeights=[5*mm, 5*mm]
    )

    table_style = TableStyle([
        ('ALIGN', (0, 0), (4, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (5, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'STSong-Light'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('LEADING', (0, 0), (-1, -1), 10),
    ])

    table.setStyle(table_style)
    table.wrapOn(pdf.get_canvas(), 180, 40)
    table.drawOn(pdf.get_canvas(), 40, 810)

    # 在第三页添加橙色填充矩形
    drawer.draw_rect(
        pos_x=90,
        pos_y=750,
        width=80,
        height=20,
        color=Colors.ORANGE,
        stroke=0,
        fill=1
    )

    # 在第三页添加文本"心理韧性"
    drawer.draw_string(
        x=95,
        y=755,
        text="心理韧性",
        font="STSong-Light",
        font_size=17,
        color=Colors.BLACK
    )

    # 在第三页添加文本"PSYCHOLOGICAL RESILIENCE"
    drawer.draw_string(
        x=87,
        y=730,
        text="PSYCHOLOGICAL RESILIENCE",
        font="Helvetica",
        font_size=15,
        color=Colors.DARK_BLUE
    )

    # 在第三页添加深蓝色填充矩形
    drawer.draw_rect(
        pos_x=420,
        pos_y=720,
        width=140,
        height=35,
        color=Colors.DARK_BLUE,
        stroke=0,
        fill=1
    )

    # 在第三页添加段落文本
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import Paragraph
    from reportlab.lib.enums import TA_JUSTIFY

    style_sheet = getSampleStyleSheet()
    para_style = ParagraphStyle(
        name="para_style",
        parent=style_sheet['Normal'],
        alignment=TA_JUSTIFY,
        fontName="STSong-Light",
        fontSize=12,
        leading=22,
        textColor=colors.black,
    )

    paragraph_text = "心理韧性 （ Resilience）是指个体在面对压力 、逆境 、创伤或重大生活挑战时能够良好适应 、快速恢复并从中成长的能力 。它反映了一个人在情绪 、认知和行为层面的抗压能力与自我调节能力 。高心理韧性者通常更乐观 、适应力强 、能有效应对不确定性。"

    para = Paragraph(paragraph_text, para_style)
    para.wrapOn(pdf.get_canvas(), 450, 70)
    para.drawOn(pdf.get_canvas(), 30, 620)

    drawer.draw_line(
        x1=25,
        y1=795,
        x2=565,
        y2=795,
        width=1,
        color=Colors.BLACK
    )
    # 在第三页绘制水平线
    drawer.draw_line(
        x1=25,
        y1=610,
        x2=565,
        y2=610,
        width=1,
        color=Colors.BLACK
    )

    # 在第三页添加文本"测评结果详情"
    drawer.draw_string(
        x=30,
        y=580,
        text="测评结果详情",
        font="STSong-Light",
        font_size=16,
        color=Colors.DARK_BLUE
    )

    # 在第三页添加文本"心理韧性等级说明"
    drawer.draw_string(
        x=30,
        y=350,
        text="心理韧性等级说明",
        font="STSong-Light",
        font_size=16,
        color=Colors.DARK_BLUE
    )

    # 在第三页绘制垂直线
    drawer.draw_line(
        x1=170,
        y1=350,
        x2=170,
        y2=350 + 16 * 1.5,  # y1 + font_size * 1.5
        width=2,
        color=Colors.DARK_BLUE
    )

    # 在第三页绘制蓝色垂直线
    drawer.draw_line(
        x1=135,
        y1=590,
        x2=135,
        y2=580,
        width=2,
        color=Colors.DARK_BLUE
    )

    # 在第三页添加文本"RESULTS DETAILS"
    drawer.draw_string(
        x=150,
        y=580,
        text="RESULTS DETAILS",
        font="Helvetica",
        font_size=14,
        color=Colors.DARK_BLUE
    )

    # 在第三页添加文本"APPLICATIONS"
    drawer.draw_string(
        x=190,
        y=350,
        text="APPLICATIONS",
        font="Helvetica",
        font_size=14,
        color=Colors.DARK_BLUE
    )

    # 在第三页添加半透明蓝色填充矩形
    drawer.draw_rect(
        pos_x=40,
        pos_y=280,
        width=160,
        height=30,
        color=Colors.DARK_BLUE,
        stroke=0,
        fill=1,
        alpha=0.7
    )

    # 在第三页添加第二个半透明蓝色填充矩形
    drawer.draw_rect(
        pos_x=40,
        pos_y=220,
        width=160,
        height=30,
        color=Colors.DARK_BLUE,
        stroke=0,
        fill=1,
        alpha=0.5
    )

    # 在第三页添加第三个半透明蓝色填充矩形
    drawer.draw_rect(
        pos_x=40,
        pos_y=160,
        width=160,
        height=30,
        color=Colors.DARK_BLUE,
        stroke=0,
        fill=1,
        alpha=0.3
    )

    # 在第三页添加文本"高 心理韧性 (42-50分)"
    drawer.draw_string(
        x=45,
        y=293,  # 285 + 8
        text="高 心理韧性 (42-50分)",
        font="STSong-Light",
        font_size=15,
        color=Colors.BLACK
    )

    # 在第三页添加文本"中等心理韧性(26 -42分)"
    drawer.draw_string(
        x=45,
        y=233,  # 225 + 8
        text="中 等心理韧性(26 -42分)",
        font="STSong-Light",
        font_size=15,
        color=Colors.BLACK
    )

    # 在第三页添加文本"低 心理韧性(10-26分)"
    drawer.draw_string(
        x=45,
        y=173,  # 165 + 8
        text="低 心理韧性(10-26分)",
        font="STSong-Light",
        font_size=15,
        color=Colors.BLACK
    )

    # 在第三页添加文本"：高心理韧性者抗挫力强、心态灵活且能快速复原，适合互联网、"
    drawer.draw_string(
        x=200,
        y=285,
        text="：高心理韧性者抗挫力强、心态灵活且能快速复原，适合互联网、",
        font="STSong-Light",
        font_size=12,
        color=Colors.BLACK
    )

    # 在第三页添加文本"：中等心理韧性者能适度承压、复原较快，适合行政、教务、常规"
    drawer.draw_string(
        x=200,
        y=230,
        text="：中等心理韧性者能适度承压、复原较快，适合行政、教务、常规",
        font="STSong-Light",
        font_size=12,
        color=Colors.BLACK
    )

    # 在第三页添加文本"金融等高压创新领域，或销售、公关等挑战型岗位。"
    drawer.draw_string(
        x=45,
        y=265,
        text="金融等高压创新领域，或销售、公关等挑战型岗位。",
        font="STSong-Light",
        font_size=12,
        color=Colors.BLACK
    )

    # 在第三页添加文本"运营等稳中有轻度挑战的岗位。"
    drawer.draw_string(
        x=45,
        y=205,
        text="运营等稳中有轻度挑战的岗位。",
        font="STSong-Light",
        font_size=12,
        color=Colors.BLACK
    )

    # 在第三页添加图片1.png
    drawer.upload_image(
        image="Design 2/1.png",
        x=30,
        y=730,
        width=None,
        height=None
    )

    # 在第三页添加右下角圆角矩形
    canvas = pdf.get_canvas()
    canvas.setStrokeColorRGB(0.5, 0.8, 1.0, alpha=0.1)  # 浅蓝色
    canvas.setFillColorRGB(0.5, 0.8, 1.0, alpha=0.1)    # 浅蓝色
    canvas.setLineWidth(0)

    # 创建右下角圆角矩形路径
    p = canvas.beginPath()
    x, y = 420, 640
    width, height = 140, 80
    radius = 15

    p.moveTo(x, y)
    p.lineTo(x + width - radius, y)
    p.lineTo(x + width, y)
    p.lineTo(x + width, y + height - radius)
    p.curveTo(x + width, y + height, x + width - radius, y + height,
              x + width - radius, y + height)
    p.lineTo(x, y + height)
    p.lineTo(x, y)

    canvas.drawPath(p, stroke=0, fill=1)

    # 在第三页添加居中文本"心理韧性测评结果"
    drawer.draw_string(
        x=490,  # 420 + 140/2 (蓝色矩形中心)
        y=730,
        text="心理韧性测评结果",
        font="STSong-Light",
        font_size=12,
        color=Colors.WHITE
    )

    # 创建第四页
    pdf.show_page()

    # 在第四页也绘制标尺
    draw_ruler(drawer, page_width, page_height)

    # 在第四页绘制水平线
    drawer.draw_line(
        x1=25,
        y1=920,
        x2=565,
        y2=920,
        width=0.5,
        color=Colors.BLACK
    )

    # 在第四页添加文本"发展建议"
    drawer.draw_string(
        x=30,
        y=885,
        text="发展建议",
        font="STSong-Light",
        font_size=18,
        color=Colors.DARK_BLUE
    )

    # 在第四页添加文本"将逐步成长为更具适应力 、 更坚韧的自己。"
    drawer.draw_string(
        x=305,
        y=625,
        text="将逐步成长为更具适应力 、 更坚韧的自己。",
        font="STSong-Light",
        font_size=18,
        color=Colors.DARK_BLUE
    )

    # 在第四页添加文本"心理韧性如同肌肉 ， 可通过科学训练不断增强 。 以下是一些建议 ，通过持续训练 ，您"
    drawer.draw_string(
        x=60,
        y=845,
        text="心理韧性如同肌肉 ， 可通过科学训练不断增强 。 以下是一些建议 ，通过持续训练 ，您",
        font="STSong-Light",
        font_size=12,
        color=Colors.BLACK
    )

    # 在第四页添加图片2.png
    drawer.upload_image(
        image="Design 2/2.png",
        x=40,
        y=695,
        width=None,
        height=None
    )

    # 在第四页添加第二个图片2.png
    drawer.upload_image(
        image="Design 2/2.png",
        x=40,
        y=545,  # 695 - 150
        width=None,
        height=None
    )

    # 在第四页添加图片4.png
    drawer.upload_image(
        image="Design 2/4.png",
        x=40,
        y=395,  # 545 - 150
        width=None,
        height=None
    )

    # 在第四页添加图片5.png
    drawer.upload_image(
        image="Design 2/5.png",
        x=40,
        y=245,  # 395 - 150
        width=None,
        height=None
    )

    # 在第四页添加图片6.png
    drawer.upload_image(
        image="Design 2/6.png",
        x=40,
        y=95,   # 245 - 150
        width=None,
        height=None
    )

    # 保存PDF
    pdf.save()
