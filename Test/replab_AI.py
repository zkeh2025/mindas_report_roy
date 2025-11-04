from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import RGBColor
from locale import normalize
from tkinter import CENTER
from fpdf.enums import Corner
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT,TA_CENTER,TA_RIGHT, TA_JUSTIFY
from reportlab.lib.colors import paleturquoise, purple, white
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
#create a page
filename = "reportlab_v1.pdf"
c = canvas.Canvas(filename)

#Roy's function library
def upload_image(c, image, x, y, width=None, height=None):
    while True:
        if width is None or height is None:
            c.drawImage(
                image,
                x = x,
                y = y,
                width = None,
                height = None,
                preserveAspectRatio=True
            )
            break
        elif isinstance(width, (int,float)) or isinstance(height, (int,float)):
            c.drawImage(
                image,
                x = x,
                y = y,
                width = width,
                height = height,
                preserveAspectRatio=False
            )
            break
        else:
            raise ValueError("width and height must be None or float")
def draw_bulltin(
    c,
    evaluation_content:list = ["推理能力", "空间能力", "加工速度", "自我概念", "思维模式", "自驱力"],
    y_start:float = 160,
    x_start:float = 0,
    r:float =5,
    x_cen:float=-12,
    y_decreament:float=20,
    y_circle_start:float=163,
    linewidth:float=0.5,
    font_size:float=23,
    ):
    for item in evaluation_content:
        #set up counter1 and counter2 with increment for position of bulltin
        y=y_start-(evaluation_content.index(item)*y_decreament)
        y_circle=y_circle_start-(evaluation_content.index(item)*y_decreament)
        
        c.setFont("STSong-Light", size = font_size)
        c.setFillColorRGB(0,0,0)
        c.setStrokeColorRGB(0,0,0)
        c.setLineWidth(linewidth*mm)
        #rotate coordinate
        c.rotate(90)
        #draw eclipse
        c.circle(y_circle*mm, x_cen*mm,r*mm,stroke=1,fill=0)
        #drawstring number counter
        
        #rotate back
        c.rotate(-90)
        #draw number in circle
        c.setFont("STSong-Light", size=font_size)
        c.setFillColorRGB(0,0,0)
        c.drawString(x_start+10*mm,y*mm,str(evaluation_content.index(item)+1))
        #draw string beside circle
        c.setFont("STSong-Light", size=font_size)
        c.setFillColorRGB(0,0,0)
        c.drawString(x_start+20*mm,y*mm,item)

        #add space between each list
def draw_line(
    x1: float,
    y1: float,
    x2: float,
    y2:float,
    width:float=1,
    color:list[float,float,float]=[0,0,0],
    ):
    c.setStrokeColorRGB(color[0],color[1],color[2])
    c.setLineWidth(width*mm)
    c.line(x1, y1, x2, y2)
def draw_string_list(
    c,
    x:float=0, y:float=0,
    r:float=0.0, g:float=0.0, b:float=0.0,
    font:str="Helvetica",
    font_size:float=50,
    label_list:list[str] = [],
    colon:str="",
    text_list:list[str] = ["B4"],
    ):
    for item in text_list:
        c.setFont(font, font_size)
        c.setFillColorRGB(r,g,b)
        if colon==":":
            c.drawString(mm*x+10, mm*y+(text_list.index(item)+1)*font_size, text = ":")
        c.drawString(mm*x+10+20, mm*y+(text_list.index(item)+1)*font_size, text = item)

    for item in label_list:
         c.drawString(mm*x, mm*y+(label_list.index(item)+1)*font_size, text = item)
def draw_string(
    c,
    x:float=0, y:float=0,
    font:str="Helvetica",
    font_size:float=50,
    color:list[float,float,float]=[0,0,0],
    text:str = ["B4"],
    ):
    c.setFont(font, font_size)
    c.setFillColorRGB(color[0],color[1],color[2])
    c.drawString(x, y, text = text)
def draw_rect(
    pos_x:float=0,
    pos_y:float=0,
    width:float=40,
    height:float=40,
    radius:float=5,
    color:list[float,float,float]=[0,0,0],
    stroke:bool=0,
    fill:bool=1,
    ):
    c.setFillColorRGB(color[0],color[1],color[2])
    c.roundRect(pos_x, pos_y, mm*width, mm*height, radius = mm*radius, \
    stroke=stroke, fill = fill)
def draw_dotted_line(
    x1: float,
    y1: float,
    x2: float,
    y2:float,
    width:float=1,
    color:list[float,float,float]=[0,0,0],
    dash:list[float,float]=[2,1],
    alpha:float=1,
    ):
    c.setStrokeColorRGB(color[0],color[1],color[2],alpha=alpha)
    c.setLineWidth(width*mm)
    c.setDash(dash)
    c.line(x1, y1, x2, y2)

cyan = [0.17255,  0.67059,  0.69804]
darkercyan= [0.18824,  0.58431,  0.50588]
black = [0,0,0]
lightcyan=[0.18824,  0.58824,  0.50588]
red=[0.70980,  0.06275,  0.12941]
lightpurple=[0.66667  ,0.69412 , 0.83137]
orange=[1.00000 , 0.63922,  0.00000]
darkblue=[0.02353 , 0.14902,  0.30980]
white=[1,1,1]

redstyle= ParagraphStyle(
    name="redstyle",
    parent=style_sheet['Normal'],
    alignment = TA_JUSTIFY,
    fontName="STSong-Light",
    fontSize=17,
    leading = 10,
    textColor=red,
)

def draw_two_table(c,x,y):
    table=Table(
        data,
        colWidths=[0.3*cm,0.3*cm,0.3*cm,0.3*cm,0.3*cm,10*cm],
        rowHeights=[0.6*cm]*2,
    )

    tablestyle=TableStyle([
        ('ALIGN',(0,0),(4,1),'CENTER'),
        ('ALIGN',(5,0),(5,1),'LEFT'),
        ('FONTNAME',(0,0),(-1,-1),'STSong-Light'),
        ('FONTSIZE',(0,0),(-1,-1),10),
    ])

    table.setStyle(tablestyle)
    table.wrapOn(c,0,0)
    table.drawOn(c,x*cm,y*cm)

blackstyle= ParagraphStyle(
    name="blackstyle",
    parent=style_sheet['Normal'],
    alignment = TA_JUSTIFY,
    fontName="STSong-Light",
    fontSize=9,
    leading = 12,
    textColor=colors.black,
)

# 初始化画布
c = canvas.Canvas("B4-核心认知能力和成长性思维-宫亦涵.pdf", pagesize=A4)
width, height = A4  # (595.27, 841.89)

# 1. 顶部机构标识
draw_string(c, 150, 800, "B4 少年 心知 DAN成长计划", "STSong-Light", 16, RGBColor(46, 74, 107))
draw_string(c, 150, 780, "PSYCHDREAM YOUNG", "Helvetica-Bold", 12, RGBColor(46, 74, 107))
draw_line(c, 100, 770, 500, 770, RGBColor(46, 74, 107), 1)

# 2. 项目名称
draw_string(c, 180, 730, "双培强基工程", "STSong-Light", 18, RGBColor(46, 74, 107))
draw_string(c, 150, 705, "青少年心理特色素质实践教育工程", "STSong-Light", 14, RGBColor(51, 51, 51))

# 3. 核心标题
draw_string(c, 120, 650, "核心认知能力和成长型思维", "STSong-Light", 22, RGBColor(211, 47, 47))
draw_string(c, 180, 620, "分析型测评包", "STSong-Light", 16, RGBColor(51, 51, 51))

# 4. 测评内容列表（居中排列）
content_list = ["推理能力", "空间能力", "加工速度", "自我概念", "思维模式", "自驱力"]
y_pos = 580
for content in content_list:
    draw_string(c, 250, y_pos, content, "STSong-Light", 14, RGBColor(51, 51, 51))
    y_pos -= 25

# 5. 标语与机构
draw_string(c, 200, 450, "发现自己 点亮未来", "STSong-Light", 16, RGBColor(46, 74, 107))
draw_string(c, 220, 425, "双培强基", "STSong-Light", 14, RGBColor(51, 51, 51))

# 6. 页脚
draw_line(c, 100, 60, 500, 60, RGBColor(153, 153, 153), 1)
draw_string(c, 100, 40, "第 1 页", "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 200, 40, "关注“双培强基工程”公众号，获取电子版报告和更多成长建议。", "STSong-Light", 10, RGBColor(102, 102, 102))

c.showPage()  # 结束第1页

# 初始化第2页画布
c = canvas.Canvas("B4-核心认知能力和成长性思维-宫亦涵.pdf", pagesize=A4)
width, height = A4

# 1. 页面标题
draw_string(c, 100, 780, "认知能力测评报告", "STSong-Light", 24, RGBColor(46, 74, 107))
draw_string(c, 100, 755, "COGNITIVE ABILITY REPORT", "Helvetica-Bold", 14, RGBColor(46, 74, 107))

# 2. 个人信息表格（双列布局）
info_col1 = [
    "姓 名:宫文学",
    "性 别:男",
    "出生日期:2008-01-08",
    "年 级:高三",
    "联系电话:139*****8182",
    "测评老师:安丽超"
]
info_col2 = [
    "档案ID:M9822936",
    "测试日期:2025-07-29 11:32:10",
    "学 校:London Central Secondary School",
    "测评单位:双培强基工程 · 素质发展研究院",
    "指导师:DAN11352",
    "报告编码:11340869020"
]
draw_two_table(c, 100, 720, info_col1, info_col2, 12, RGBColor(51, 51, 51))

# 3. 认知能力定义
draw_string(c, 100, 600, "认知能力 丨 COGNITIVE ABILITY", "STSong-Light", 16, RGBColor(211, 47, 47))
cog_def = "认知能力是大脑加工、处理信息，认知客观事物内部逻辑，并运用知识、经验等解决问题的能力。认知的过程包括感知、记忆、想象、思考、判断等。它被重视的原因是人类所有的学习活动都离不开认知能力的运用。"
draw_paragraph(c, 100, 570, 400, cog_def, "STSong-Light", 11, RGBColor(51, 51, 51))

# 4. 总得分与百分位
draw_string(c, 100, 510, "认知能力测评结果 丨 Results Summary", "STSong-Light", 16, RGBColor(211, 47, 47))
draw_string(c, 150, 480, "总得分 Total Score: 122", "STSong-Light", 14, RGBColor(51, 51, 51))
draw_string(c, 150, 450, "百分位(%) Percentile: 92", "STSong-Light", 14, RGBColor(51, 51, 51))
draw_string(c, 150, 420, "您在认知能力上的总分数超过了85%的同龄人", "STSong-Light", 12, RGBColor(46, 74, 107))

# 5. 正态分布图占位（按文档刻度绘制边框）
draw_rect(c, 100, 350, 400, 80, RGBColor(245, 245, 245), RGBColor(153, 153, 153), 1)
draw_string(c, 250, 410, "正态分布图 丨 TOTAL SCORE", "STSong-Light", 12, RGBColor(102, 102, 102))
# 刻度标注（匹配文档第2-51段）
scale_x = [100, 150, 200, 250, 300, 350, 400, 450, 500]
scale_labels = ["62", "70", "78", "85", "92", "100", "108", "116", "124"]
for x, label in zip(scale_x, scale_labels):
    draw_string(c, x, 345, label, "Helvetica", 8, RGBColor(102, 102, 102))

# 6. 二维码区域（右侧）
draw_rect(c, 450, 650, 80, 80, RGBColor(255, 255, 255), RGBColor(153, 153, 153), 1)
draw_string(c, 440, 640, "扫二维码", "STSong-Light", 10, RGBColor(51, 51, 51))
draw_string(c, 420, 625, "保存孩子电子报告观看专家成长建议", "STSong-Light", 8, RGBColor(51, 51, 51))

# 7. 页脚
draw_line(c, 100, 60, 500, 60, RGBColor(153, 153, 153), 1)
draw_string(c, 100, 40, "第 2 页", "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 200, 40, "关注“双培强基工程”公众号，获取电子版报告和更多成长建议。", "STSong-Light", 10, RGBColor(102, 102, 102))

c.showPage()  # 结束第2页

# 初始化第3页画布
c = canvas.Canvas("B4-核心认知能力和成长性思维-宫亦涵.pdf", pagesize=A4)
width, height = A4

# 1. 页面标题
draw_string(c, 100, 780, "感知觉报告", "STSong-Light", 24, RGBColor(46, 74, 107))
draw_string(c, 100, 755, "PERCEPTION REPORT", "Helvetica-Bold", 14, RGBColor(46, 74, 107))

# 2. 个人信息栏（精简版）
info_col1 = ["姓 名:宫文学", "档案ID:M9822936", "测试时间:2025-07-29"]
info_col2 = ["出生日期:2008-01-08", "指导师:DAN11352", "报告编码:11340869020"]
draw_two_table(c, 100, 720, info_col1, info_col2, 12, RGBColor(51, 51, 51))

# 3. 感知觉定义
draw_string(c, 100, 650, "感知觉 丨 PERCEPTION", "STSong-Light", 16, RGBColor(211, 47, 47))
percep_def = "感知觉是大脑对作用于感觉器官的客观事物的整体感知，是记忆、推理等后续大脑信息加工的基础。人们通过感知、观察认识世界。人类众多伟大的科学发现都依赖于科学家敏锐和细致的观察。"
draw_paragraph(c, 100, 620, 400, percep_def, "STSong-Light", 11, RGBColor(51, 51, 51))

# 4. 个人得分
draw_string(c, 100, 560, "我的感知觉得分", "STSong-Light", 14, RGBColor(51, 51, 51))
draw_string(c, 150, 530, "31 丨 98%", "Helvetica-Bold", 16, RGBColor(211, 47, 47))
# 得分对比刻度（匹配文档第2-116段）
draw_rect(c, 100, 500, 400, 20, RGBColor(245, 245, 245), RGBColor(153, 153, 153), 1)
draw_string(c, 120, 495, "21.2", "Helvetica", 8, RGBColor(102, 102, 102))
draw_string(c, 250, 495, "21.6", "Helvetica", 8, RGBColor(102, 102, 102))
draw_string(c, 400, 495, "31", "Helvetica", 8, RGBColor(211, 47, 47))

# 5. 发展表现
draw_string(c, 100, 460, "发展表现 丨 DEVELOPMENTAL CHARACTERISTICS", "STSong-Light", 16, RGBColor(211, 47, 47))
high_perf = ["高分表现：", "目光敏锐，头脑清楚", "明察秋毫，洞察力强", "眼观六路耳听八方"]
low_perf = ["低分表现：", "粗心大意，走马观花", "丢三落四，敷衍了事", "马马虎虎，不求甚解"]
draw_two_table(c, 100, 430, high_perf, low_perf, 11, RGBColor(51, 51, 51))

# 6. 成长建议
draw_string(c, 100, 350, "成长建议 丨 GROWTH ADVICE", "STSong-Light", 16, RGBColor(211, 47, 47))
advice = "观察力的培养可以从两个维度着手：\n1. 挖掘内在动力：保持好奇（本能探索欲）、培养兴趣（关注感兴趣领域，思维更活跃）；\n2. 培养外在习惯：绘画训练（“惟妙惟肖”的绘画依赖敏锐观察，长期训练有益感知觉提升）。"
draw_paragraph(c, 100, 320, 400, advice, "STSong-Light", 11, RGBColor(51, 51, 51))

# 7. 页脚
draw_line(c, 100, 60, 500, 60, RGBColor(153, 153, 153), 1)
draw_string(c, 100, 40, "第 3 页", "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 200, 40, "关注“双培强基工程”公众号，获取电子版报告和更多成长建议。", "STSong-Light", 10, RGBColor(102, 102, 102))

c.showPage()  # 结束第3页

# 初始化第4页画布
c = canvas.Canvas("B4-核心认知能力和成长性思维-宫亦涵.pdf", pagesize=A4)
width, height = A4

# 1. 页面标题
draw_string(c, 100, 780, "记忆力报告", "STSong-Light", 24, RGBColor(46, 74, 107))
draw_string(c, 100, 755, "MEMORY REPORT", "Helvetica-Bold", 14, RGBColor(46, 74, 107))

# 2. 个人信息栏
info_col1 = ["姓 名:宫文学", "档案ID:M9822936", "测试时间:2025-07-29"]
info_col2 = ["出生日期:2008-01-08", "指导师:DAN11352", "报告编码:11340869020"]
draw_two_table(c, 100, 720, info_col1, info_col2, 12, RGBColor(51, 51, 51))

# 3. 记忆力定义
draw_string(c, 100, 650, "记忆力 丨 MEMORY", "STSong-Light", 16, RGBColor(211, 47, 47))
memory_def = "记忆力是神经系统存储过往经验的能力。记单词，背公式均和记忆力有关。人的记忆力存在先天差异，有些人看一遍就记住了，有些人要看3-5遍才能记住；有些人当时记住了，但很快就忘记了，而有些人一旦记住，就很难忘记。"
draw_paragraph(c, 100, 620, 400, memory_def, "STSong-Light", 11, RGBColor(51, 51, 51))

# 4. 个人得分
draw_string(c, 100, 560, "我的记忆力得分", "STSong-Light", 14, RGBColor(51, 51, 51))
draw_string(c, 150, 530, "28 丨 98%", "Helvetica-Bold", 16, RGBColor(211, 47, 47))
# 得分对比刻度（匹配文档第2-146段）
draw_rect(c, 100, 500, 400, 20, RGBColor(245, 245, 245), RGBColor(153, 153, 153), 1)
draw_string(c, 120, 495, "17", "Helvetica", 8, RGBColor(102, 102, 102))
draw_string(c, 250, 495, "17.5", "Helvetica", 8, RGBColor(102, 102, 102))
draw_string(c, 400, 495, "28", "Helvetica", 8, RGBColor(211, 47, 47))

# 5. 发展表现
draw_string(c, 100, 460, "发展表现 丨 DEVELOPMENTAL CHARACTERISTICS", "STSong-Light", 16, RGBColor(211, 47, 47))
high_perf = ["高分表现：", "记忆力强，记住速度快", "记忆深刻，不易忘记", "极少数人甚至过目不忘"]
low_perf = ["低分表现：", "记不住，学不会；记不清，记混", "当时记住了，但很快忘记"]
draw_two_table(c, 100, 430, high_perf, low_perf, 11, RGBColor(51, 51, 51))

# 6. 成长建议
draw_string(c, 100, 350, "成长建议 丨 GROWTH ADVICE", "STSong-Light", 16, RGBColor(211, 47, 47))
advice = "从记忆过程来看，记忆分为“记”和“忆”两个部分：\n1. “记”（编码与存储）：有规律的间隔复习（强化长期记忆）、知识关联（画思维导图，建立多维度联系）；\n2. “忆”（检索与取出）：输出讲解（做小老师，讲给他人听，巩固记忆+深化理解）、睡前回忆（复盘当日知识，检验记忆效果）。"
draw_paragraph(c, 100, 320, 400, advice, "STSong-Light", 11, RGBColor(51, 51, 51))

# 7. 页脚
draw_line(c, 100, 60, 500, 60, RGBColor(153, 153, 153), 1)
draw_string(c, 100, 40, "第 4 页", "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 200, 40, "关注“双培强基工程”公众号，获取电子版报告和更多成长建议。", "STSong-Light", 10, RGBColor(102, 102, 102))

c.showPage()  # 结束第4页

# 初始化第5页画布
c = canvas.Canvas("B4-核心认知能力和成长性思维-宫亦涵.pdf", pagesize=A4)
width, height = A4

# 1. 页面标题
draw_string(c, 100, 780, "注意力报告", "STSong-Light", 24, RGBColor(46, 74, 107))
draw_string(c, 100, 755, "ATTENTION REPORT", "Helvetica-Bold", 14, RGBColor(46, 74, 107))

# 2. 个人信息栏
info_col1 = ["姓 名:宫文学", "档案ID:M9822936", "测试时间:2025-07-29"]
info_col2 = ["出生日期:2008-01-08", "指导师:DAN11352", "报告编码:11340869020"]
draw_two_table(c, 100, 720, info_col1, info_col2, 12, RGBColor(51, 51, 51))

# 3. 注意力定义
draw_string(c, 100, 650, "注意力 丨 ATTENTION", "STSong-Light", 16, RGBColor(211, 47, 47))
attention_def = "注意是心理活动对一定对象的指向和集中。注意就像一个聚光灯，打在关注的事物上，有的人聚光能力强，有的人聚光涣散。聚光能力的发展就是注意力的好和坏。上课常常走神，做作业时常坐不住，都可能和注意力有关。"
draw_paragraph(c, 100, 620, 400, attention_def, "STSong-Light", 11, RGBColor(51, 51, 51))

# 4. 个人得分
draw_string(c, 100, 560, "我的注意力得分", "STSong-Light", 14, RGBColor(51, 51, 51))
draw_string(c, 150, 530, "77 丨 60%", "Helvetica-Bold", 16, RGBColor(211, 47, 47))
# 得分对比刻度（匹配文档第2-178段）
draw_rect(c, 100, 500, 400, 20, RGBColor(245, 245, 245), RGBColor(153, 153, 153), 1)
draw_string(c, 120, 495, "73.75", "Helvetica", 8, RGBColor(102, 102, 102))
draw_string(c, 250, 495, "75", "Helvetica", 8, RGBColor(102, 102, 102))
draw_string(c, 400, 495, "77", "Helvetica", 8, RGBColor(211, 47, 47))

# 5. 发展表现
draw_string(c, 100, 460, "发展表现 丨 DEVELOPMENTAL CHARACTERISTICS", "STSong-Light", 16, RGBColor(211, 47, 47))
high_perf = ["高分表现：", "安静、专注，上课少有走神", "注意力稳定，不易被外在事物干扰", "注意范围广，能察觉更多信息", "注意转移灵活，快速转入下一活动"]
low_perf = ["低分表现：", "注意力不集中，注意力涣散", "注意力狭窄，作业、考试漏题", "心不在焉，上课、做作业经常走神", "好动，坐不住，无法长时间专注"]
draw_two_table(c, 100, 430, high_perf, low_perf, 11, RGBColor(51, 51, 51))

# 6. 成长建议
draw_string(c, 100, 330, "成长建议 丨 GROWTH ADVICE", "STSong-Light", 16, RGBColor(211, 47, 47))
advice = "培养注意力从两方面入手：\n1. 减少干扰：建立专属清净空间（减少家人干扰）、控制电子设备使用（避免破坏专注力）；\n2. 培养习惯：学习规划（设定具体目标+时间计划，增强专注）、番茄钟（限定时间只做一件事，强化专注节奏）。"
draw_paragraph(c, 100, 300, 400, advice, "STSong-Light", 11, RGBColor(51, 51, 51))

# 7. 页脚
draw_line(c, 100, 60, 500, 60, RGBColor(153, 153, 153), 1)
draw_string(c, 100, 40, "第 5 页", "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 200, 40, "关注“双培强基工程”公众号，获取电子版报告和更多成长建议。", "STSong-Light", 10, RGBColor(102, 102, 102))

c.showPage()  # 结束第5页

# 初始化第6页画布
c = canvas.Canvas("B4-核心认知能力和成长性思维-宫亦涵.pdf", pagesize=A4)
width, height = A4

# 1. 页面标题
draw_string(c, 100, 780, "推理能力报告", "STSong-Light", 24, RGBColor(46, 74, 107))
draw_string(c, 100, 755, "REASONING REPORT", "Helvetica-Bold", 14, RGBColor(46, 74, 107))

# 2. 个人信息栏
info_col1 = ["姓 名:宫文学", "档案ID:M9822936", "测试时间:2025-07-29"]
info_col2 = ["出生日期:2008-01-08", "指导师:DAN11352", "报告编码:11340869020"]
draw_two_table(c, 100, 720, info_col1, info_col2, 12, RGBColor(51, 51, 51))

# 3. 推理能力定义
draw_string(c, 100, 650, "推理能力 丨 REASONING", "STSong-Light", 16, RGBColor(211, 47, 47))
reason_def = "推理是指一个人通过已有知识和经验，通过分析和综合做出新判断的过程。推理能力是一个人学习的关键，也工作和生活中解决问题能力的核心。我们常提到的“逻辑思维能力”其背后的关键是推理能力。"
draw_paragraph(c, 100, 620, 400, reason_def, "STSong-Light", 11, RGBColor(51, 51, 51))

# 4. 个人得分
draw_string(c, 100, 560, "我的推理能力得分", "STSong-Light", 14, RGBColor(51, 51, 51))
draw_string(c, 150, 530, "36 丨 86%", "Helvetica-Bold", 16, RGBColor(211, 47, 47))
# 得分对比刻度（匹配文档第2-207段）
draw_rect(c, 100, 500, 400, 20, RGBColor(245, 245, 245), RGBColor(153, 153, 153), 1)
draw_string(c, 120, 495, "28.75", "Helvetica", 8, RGBColor(102, 102, 102))
draw_string(c, 250, 495, "28.75", "Helvetica", 8, RGBColor(102, 102, 102))
draw_string(c, 400, 495, "36", "Helvetica", 8, RGBColor(211, 47, 47))

# 5. 发展表现
draw_string(c, 100, 460, "发展表现 丨 DEVELOPMENTAL CHARACTERISTICS", "STSong-Light", 16, RGBColor(211, 47, 47))
high_perf = ["高分表现：", "理解能力强，学习速度快，问题解决能力强", "主次分明，目标明确，偏好认知刺激", "思路清晰，有理有据，有条不紊", "兴趣广泛，求知欲强，独立思考，挑战权威"]
low_perf = ["低分表现：", "理解能力偏弱，学习效率低，问题解决能力弱", "理不清重点，易陷细节，目标模糊", "词语言简单，逻辑混乱，前言不搭后语", "兴趣狭窄，偏好简单事物，墨守成规"]
draw_two_table(c, 100, 430, high_perf, low_perf, 11, RGBColor(51, 51, 51))

# 6. 成长建议
draw_string(c, 100, 320, "成长建议 丨 GROWTH ADVICE", "STSong-Light", 16, RGBColor(211, 47, 47))
advice = "推理能力的核心是发现事物关系+逻辑表达：\n1. 善用思维工具：用思维导图梳理每日/每周知识（“串知识”即梳理关系，养成逻辑习惯）；\n2. 有逻辑的表达：沟通前先在脑中排序观点（123优先级或前因后果），再讲给他人听，强化逻辑输出。"
draw_paragraph(c, 100, 290, 400, advice, "STSong-Light", 11, RGBColor(51, 51, 51))

# 7. 页脚
draw_line(c, 100, 60, 500, 60, RGBColor(153, 153, 153), 1)
draw_string(c, 100, 40, "第 6 页", "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 200, 40, "关注“双培强基工程”公众号，获取电子版报告和更多成长建议。", "STSong-Light", 10, RGBColor(102, 102, 102))

c.showPage()  # 结束第6页

# 初始化第7页画布
c = canvas.Canvas("B4-核心认知能力和成长性思维-宫亦涵.pdf", pagesize=A4)
width, height = A4

# 1. 页面标题
draw_string(c, 100, 780, "空间能力报告", "STSong-Light", 24, RGBColor(46, 74, 107))
draw_string(c, 100, 755, "SPATIAL ABILITY REPORT", "Helvetica-Bold", 14, RGBColor(46, 74, 107))

# 2. 个人信息栏
info_col1 = ["姓 名:宫文学", "档案ID:M9822936", "测试时间:2025-07-29"]
info_col2 = ["出生日期:2008-01-08", "指导师:DAN11352", "报告编码:11340869020"]
draw_two_table(c, 100, 720, info_col1, info_col2, 12, RGBColor(51, 51, 51))

# 3. 空间能力定义
draw_string(c, 100, 650, "空间能力 丨 SPATIAL ABILITY", "STSong-Light", 16, RGBColor(211, 47, 47))
spatial_def = "空间能力是指大脑通过观察、触摸及想象对物体形状、位置或运动状态判断的能力。空间能力对一个人在数学、自然科学、工程、气象、化学和物理等科学领域取得成功至关重要。"
draw_paragraph(c, 100, 620, 400, spatial_def, "STSong-Light", 11, RGBColor(51, 51, 51))

# 4. 个人得分
draw_string(c, 100, 560, "我的空间能力得分", "STSong-Light", 14, RGBColor(51, 51, 51))
draw_string(c, 150, 530, "24 丨 63%", "Helvetica-Bold", 16, RGBColor(211, 47, 47))
# 得分对比刻度（匹配文档第2-234段）
draw_rect(c, 100, 500, 400, 20, RGBColor(245, 245, 245), RGBColor(153, 153, 153), 1)
draw_string(c, 120, 495, "21.6", "Helvetica", 8, RGBColor(102, 102, 102))
draw_string(c, 250, 495, "21.9", "Helvetica", 8, RGBColor(102, 102, 102))
draw_string(c, 400, 495, "24", "Helvetica", 8, RGBColor(211, 47, 47))

# 5. 发展表现
draw_string(c, 100, 460, "发展表现 丨 DEVELOPMENTAL CHARACTERISTICS", "STSong-Light", 16, RGBColor(211, 47, 47))
high_perf = ["高分表现：", "空间方向感更好，擅长数学思考和运算", "空间想象力丰富，易对绘画、设计产生兴趣"]
low_perf = ["低分表现：", "空间方向感差", "在抽象的数学运算上表现差"]
draw_two_table(c, 100, 430, high_perf, low_perf, 11, RGBColor(51, 51, 51))

# 6. 成长建议
draw_string(c, 100, 380, "成长建议 丨 GROWTH ADVICE", "STSong-Light", 16, RGBColor(211, 47, 47))
advice = "空间能力兼具天赋与后天训练：\n1. 天赋发挥（若有优势）：参与积木乐高、奥数竞赛等挑战性项目，强化空间思维；\n2. 后天提升（一般水平）：多动手（剪纸、折纸）、多观察（对比物体形状/位置）、多创作（绘画，表达空间关系），具体可通过“拼一拼、转一转、剪一剪、折一折、画一画”训练。"
draw_paragraph(c, 100, 350, 400, advice, "STSong-Light", 11, RGBColor(51, 51, 51))

# 7. 页脚
draw_line(c, 100, 60, 500, 60, RGBColor(153, 153, 153), 1)
draw_string(c, 100, 40, "第 7 页", "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 200, 40, "关注“双培强基工程”公众号，获取电子版报告和更多成长建议。", "STSong-Light", 10, RGBColor(102, 102, 102))

c.showPage()  # 结束第7页

# 初始化第8页画布
c = canvas.Canvas("B4-核心认知能力和成长性思维-宫亦涵.pdf", pagesize=A4)
width, height = A4

# 1. 页面标题
draw_string(c, 100, 780, "加工速度报告", "STSong-Light", 24, RGBColor(46, 74, 107))
draw_string(c, 100, 755, "PROCESSING SPEED REPORT", "Helvetica-Bold", 14, RGBColor(46, 74, 107))

# 2. 个人信息栏
info_col1 = ["姓 名:宫文学", "档案ID:M9822936", "测试时间:2025-07-29"]
info_col2 = ["出生日期:2008-01-08", "指导师:DAN11352", "报告编码:11340869020"]
draw_two_table(c, 100, 720, info_col1, info_col2, 12, RGBColor(51, 51, 51))

# 3. 加工速度定义
draw_string(c, 100, 650, "加工速度 丨 PROCESSING SPEED", "STSong-Light", 16, RGBColor(211, 47, 47))
speed_def = "加工速度是指一个人大脑接受信息、处理信息和做出反应的速度。如果将大脑比作一台计算机，那么加工速度就是电脑的运行速度。在面对复杂问题时，加工速度对认知加工效率的影响更明显。对于加工速度慢的人，过大的信息量还可能导致大脑“卡机”。"
draw_paragraph(c, 100, 620, 400, speed_def, "STSong-Light", 11, RGBColor(51, 51, 51))

# 4. 个人得分
draw_string(c, 100, 560, "我的加工速度得分", "STSong-Light", 14, RGBColor(51, 51, 51))
draw_string(c, 150, 530, "34 丨 86%", "Helvetica-Bold", 16, RGBColor(211, 47, 47))
# 得分对比刻度（匹配文档第2-267段）
draw_rect(c, 100, 500, 400, 40, RGBColor(245, 245, 245), RGBColor(153, 153, 153), 1)
draw_string(c, 120, 495, "28", "Helvetica", 8, RGBColor(102, 102, 102))
draw_string(c, 250, 495, "44", "Helvetica", 8, RGBColor(102, 102, 102))
draw_string(c, 400, 495, "34", "Helvetica", 8, RGBColor(211, 47, 47))
draw_string(c, 120, 475, "28", "Helvetica", 8, RGBColor(102, 102, 102))
draw_string(c, 250, 475, "44", "Helvetica", 8, RGBColor(102, 102, 102))
draw_string(c, 400, 475, "34", "Helvetica", 8, RGBColor(211, 47, 47))

# 5. 发展表现
draw_string(c, 100, 440, "发展表现 丨 DEVELOPMENTAL CHARACTERISTICS", "STSong-Light", 16, RGBColor(211, 47, 47))
high_perf = ["高分表现：", "思维敏捷、反应迅速", "做事专注", "喜欢信息量大、有挑战的事"]
low_perf = ["低分表现：", "思维迟钝、反应慢", "容易走神", "偏好做简单、熟悉或重复的事"]
draw_two_table(c, 100, 410, high_perf, low_perf, 11, RGBColor(51, 51, 51))

# 6. 成长建议
draw_string(c, 100, 350, "成长建议 丨 GROWTH ADVICE", "STSong-Light", 16, RGBColor(211, 47, 47))
advice = "加工速度与年龄、遗传、熟悉度相关，可通过两方面提升：\n1. 多练习（特定领域）：针对目标领域反复练习（如键盘打字，从“单字母敲”到“盲打”，熟练提升速度）；\n2. 多运动（整体提升）：参与有氧运动（运动产生神经营养因子，促进神经发育，加快大脑信息传递）。"
draw_paragraph(c, 100, 320, 400, advice, "STSong-Light", 11, RGBColor(51, 51, 51))

# 7. 页脚
draw_line(c, 100, 60, 500, 60, RGBColor(153, 153, 153), 1)
draw_string(c, 100, 40, "第 8 页", "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 200, 40, "关注“双培强基工程”公众号，获取电子版报告和更多成长建议。", "STSong-Light", 10, RGBColor(102, 102, 102))

c.showPage()  # 结束第8页

# 初始化第9页画布
c = canvas.Canvas("B4-核心认知能力和成长性思维-宫亦涵.pdf", pagesize=A4)
width, height = A4

# 1. 页面标题
draw_string(c, 100, 780, "自我概念测评报告", "STSong-Light", 24, RGBColor(46, 74, 107))
draw_string(c, 100, 755, "SELF-CONCEPT REPORT", "Helvetica-Bold", 14, RGBColor(46, 74, 107))

# 2. 个人信息栏
info_col1 = ["姓 名:宫文学", "档案ID:M9822936", "测试时间:2025-07-29"]
info_col2 = ["出生日期:2008-01-08", "指导师:DAN11352", "报告编码:11340869020"]
draw_two_table(c, 100, 720, info_col1, info_col2, 12, RGBColor(51, 51, 51))

# 3. 自我概念定义
draw_string(c, 100, 650, "自我概念 丨 SELF-CONCEPT", "STSong-Light", 16, RGBColor(211, 47, 47))
self_def = "自我概念是个体对自己认识的集合，个体认为的“我是谁，我是一个怎样的人”。也可以理解为个人心中对自己的印象，包括对身体、能力、性格、态度等。比如“我是聪明的”“我是漂亮的”“我学习好”。自我概念的发展过程是一个人个性形成和社会化发展的关键。自我概念具有重要的动机属性，例如一个认为“我学习好”的人很难接受自己成绩差，即使偶尔考的差，也会通过努力来提高成绩，保持自我概念的一致性；相反，一个认为“我学习差”的人，这种定性的认识会让人懈怠、自暴自弃，从而成绩更差，形成恶性循环。"
draw_paragraph(c, 100, 600, 400, self_def, "STSong-Light", 11, RGBColor(51, 51, 51))

# 4. 测评结果详情（六大维度）
draw_string(c, 100, 500, "测评结果详情 丨 RESULTS DETAILS", "STSong-Light", 16, RGBColor(211, 47, 47))
dimensions = [
    "行为表现 Behavioral adjustment",
    "能力与学校表现 Intellectual And School Status",
    "躯体外貌 Physical Appearance And Attributes",
    "情绪状态 Freedom From Anxiety",
    "合群 Popularity",
    "幸福与满足 Happiness And Satisfaction"
]
# 绘制维度得分表（匹配文档第2-311段，得分均为10）
draw_rect(c, 100, 420, 400, 80, RGBColor(245, 245, 245), RGBColor(153, 153, 153), 1)
y_pos = 480
for dim in dimensions:
    draw_string(c, 120, y_pos, dim, "STSong-Light", 10, RGBColor(51, 51, 51))
    draw_string(c, 450, y_pos, "10", "Helvetica-Bold", 10, RGBColor(211, 47, 47))
    y_pos -= 13

# 5. 评分标准标注
score_labels = ["偏低 Low", "正常 Normal", "偏高 High"]
draw_string(c, 150, 400, score_labels[0], "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 270, 400, score_labels[1], "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 390, 400, score_labels[2], "STSong-Light", 10, RGBColor(102, 102, 102))

# 6. 页脚
draw_line(c, 100, 60, 500, 60, RGBColor(153, 153, 153), 1)
draw_string(c, 100, 40, "第 9 页", "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 200, 40, "关注“双培强基工程”公众号，获取电子版报告和更多成长建议。", "STSong-Light", 10, RGBColor(102, 102, 102))

c.showPage()  # 结束第9页

# 初始化第10页画布
c = canvas.Canvas("B4-核心认知能力和成长性思维-宫亦涵.pdf", pagesize=A4)
width, height = A4

# 1. 页面标题
draw_string(c, 100, 780, "自我概念与个人发展", "STSong-Light", 24, RGBColor(46, 74, 107))
draw_string(c, 100, 755, "SELF-CONCEPT AND PERSONAL DEVELOPMENT", "Helvetica-Bold", 14, RGBColor(46, 74, 107))

# 2. 自我概念发展圈（核心图表）
draw_string(c, 100, 720, "自我概念发展圈", "STSong-Light", 16, RGBColor(211, 47, 47))
# 绘制圆形布局（模拟文档第2-316段逻辑）
draw_rect(c, 150, 500, 300, 200, RGBColor(245, 245, 245), RGBColor(153, 153, 153), 1)
# 四个核心节点
nodes = [
    ("我眼中的我\nI IN MY EYES", 250, 670),
    ("我的行为\nMY BEHAVIOR", 400, 570),
    ("别人眼中的我\nI AM IN THE EYES OF OTHERS", 250, 470),
    ("别人对我的反应\nPEOPLE'S REACTION TO ME", 100, 570)
]
for text, x, y in nodes:
    draw_rect(c, x-60, y-20, 120, 40, RGBColor(255, 255, 255), RGBColor(46, 74, 107), 1)
    draw_paragraph(c, x-55, y-15, 110, text, "STSong-Light", 9, RGBColor(46, 74, 107))
# 箭头连接（表示循环关系）
draw_line(c, 250, 650, 350, 590, RGBColor(211, 47, 47), 1)  # 我眼中的我→我的行为
draw_line(c, 400, 570, 350, 490, RGBColor(211, 47, 47), 1)  # 我的行为→别人眼中的我
draw_line(c, 250, 490, 150, 550, RGBColor(211, 47, 47), 1)  # 别人眼中的我→别人的反应
draw_line(c, 100, 570, 150, 630, RGBColor(211, 47, 47), 1)  # 别人的反应→我眼中的我

# 3. 积极与消极自我概念对比
draw_string(c, 100, 450, "自我概念类型对比", "STSong-Light", 16, RGBColor(211, 47, 47))
high_perf = ["积极自我概念：", "感觉自己有能力，用行动印证感受", "他人给予积极反应，强化积极自我认知", "形成“积极感受→积极行动→积极反馈”循环"]
low_perf = ["消极自我概念：", "对自己能力缺乏信心，影响行动", "他人给予消极反应，强化消极自我认知", "形成“消极感受→消极行动→消极反馈”循环"]
draw_two_table(c, 100, 420, high_perf, low_perf, 11, RGBColor(51, 51, 51))

# 4. 成长建议
draw_string(c, 100, 340, "成长建议：劫持“自我概念发展圈” 丨 GROWTH ADVICE", "STSong-Light", 16, RGBColor(211, 47, 47))
advice = "自我概念在互动中发展，提升关键是打破循环：\n1. 给家长和老师的建议：少负面反馈（避免只关注短板，减少消极暗示）、多技能支持（培养执行功能、目标拆解、时间管理等能力，支撑孩子完成目标）；\n2. 给孩子的建议：找到你的强项（运用强项获得成就感，积累积极体验）、自我反省（以新视角看待自己，发展更强大的自我认知）。"
draw_paragraph(c, 100, 310, 400, advice, "STSong-Light", 11, RGBColor(51, 51, 51))

# 5. 页脚
draw_line(c, 100, 60, 500, 60, RGBColor(153, 153, 153), 1)
draw_string(c, 100, 40, "第 10 页", "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 200, 40, "关注“双培强基工程”公众号，获取电子版报告和更多成长建议。", "STSong-Light", 10, RGBColor(102, 102, 102))

c.showPage()  # 结束第10页

# 初始化第11页画布
c = canvas.Canvas("B4-核心认知能力和成长性思维-宫亦涵.pdf", pagesize=A4)
width, height = A4

# 1. 页面标题
draw_string(c, 100, 780, "固定型与成长型思维模式测评报告", "STSong-Light", 24, RGBColor(46, 74, 107))
draw_string(c, 100, 755, "FIXED AND GROWTH MINDSET REPORT", "Helvetica-Bold", 14, RGBColor(46, 74, 107))

# 2. 个人信息栏
info_col1 = ["姓 名:宫文学", "档案ID:M9822936", "测试时间:2025-07-29"]
info_col2 = ["出生日期:2008-01-08", "指导师:DAN11352", "报告编码:11340869020"]
draw_two_table(c, 100, 720, info_col1, info_col2, 12, RGBColor(51, 51, 51))

# 3. 思维模式定义
draw_string(c, 100, 650, "固定型与成长型思维模式 丨 FIXED AND GROWTH MINDSET", "STSong-Light", 16, RGBColor(211, 47, 47))
mindset_def = "思维模式是一种信念，潜移默化的影响着一个人的成长，塑造一个人的学习能力。心理学家将人的思维模式分为两种——固定型和成长型思维模式。固定型思维模式的人认为人的能力是天生不变的，成长型思维模式的人认为人的能力是可以通过学习提高的，人可以通过努力达成目标。"
draw_paragraph(c, 100, 620, 400, mindset_def, "STSong-Light", 11, RGBColor(51, 51, 51))

# 4. 思维模式自我证明逻辑
draw_string(c, 100, 560, "思维模式的自我证明", "STSong-Light", 16, RGBColor(211, 47, 47))
logic_text = "你对自己的信念决定了你对一些事的态度，你的态度又影响你做事的结果，做事的结果又再次影响你的信念。因此，你会一遍又一遍证明自己最初的信念，最后你就成为了那样的人。"
draw_paragraph(c, 100, 530, 400, logic_text, "STSong-Light", 11, RGBColor(51, 51, 51))

# 5. 两种思维模式核心差异（双列表格）
draw_string(c, 100, 480, "思维模式核心差异对比", "STSong-Light", 14, RGBColor(51, 51, 51))
compare_cols = [
    ["成长型思维模式", "信念：我可以提高我的能力", "态度：拥抱挑战，努力坚持", "面对错误：感激引导，从中学习", "面对障碍：坚持不懈", "最终结果：提高能力，取得更高成就"],
    ["固定型思维模式", "信念：我能力就这样了，不会变", "态度：避免挑战，后退放弃", "面对错误：气馁，避免犯错", "面对障碍：轻易放弃", "最终结果：停滞不前，不能发挥潜力"]
]
draw_two_table(c, 100, 450, compare_cols[0], compare_cols[1], 11, RGBColor(51, 51, 51))

# 6. 页脚
draw_line(c, 100, 60, 500, 60, RGBColor(153, 153, 153), 1)
draw_string(c, 100, 40, "第 11 页", "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 200, 40, "关注“双培强基工程”公众号，获取电子版报告和更多成长建议。", "STSong-Light", 10, RGBColor(102, 102, 102))

c.showPage()  # 结束第11页

# 初始化第12页画布
c = canvas.Canvas("B4-核心认知能力和成长性思维-宫亦涵.pdf", pagesize=A4)
width, height = A4

# 1. 页面标题
draw_string(c, 100, 780, "专家建议：培养成长型思维模式", "STSong-Light", 24, RGBColor(46, 74, 107))
draw_string(c, 100, 755, "GROWTH ADVICE: DEVELOP GROWTH MINDSET", "Helvetica-Bold", 14, RGBColor(46, 74, 107))

# 2. 建议核心逻辑
core_advice = "培养成长型思维模式，即让孩子形成“我可以通过努力提高能力，困难面前能克服”的信念。首先，家长老师需先有此信念；其次，通过沟通引导强化孩子的信念，具体可参考以下“如何说”与“不要说”的建议。"
draw_paragraph(c, 100, 720, 400, core_advice, "STSong-Light", 11, RGBColor(51, 51, 51))

# 3. “如何说”（积极引导话术）
draw_string(c, 100, 660, "如何说（积极引导）", "STSong-Light", 16, RGBColor(46, 74, 107))
positive_lines = [
    "1. 当你学习解决新问题时，你的大脑在成长，你的能力在提高。",
    "2. 如果你发现自己在说“我不擅长学习”，就在开头加上“还”：“我还不擅长学习”。",
    "3. 感觉学习难是因为我的大脑在成长，我的能力在提高。",
    "4. 重点不是马上考高分，关键是一步步提高学习能力——想下一步能做什么、如何提高效率、谁能提供帮助。"
]
y_pos = 630
for line in positive_lines:
    draw_string(c, 120, y_pos, line, "STSong-Light", 11, RGBColor(51, 51, 51))
    y_pos -= 25

# 4. “不要说”（避免消极话术）
draw_string(c, 100, 520, "不要说（避免消极）", "STSong-Light", 16, RGBColor(211, 47, 47))
negative_lines = [
    "1. 不是每个人都擅长这个，尽力就好。",
    "2. 没关系，也许学习不是你的强项。",
    "3. 别担心，如果你继续努力，你会成功的。（注：无方法支持的努力可能无效，易让孩子觉得无能）",
    "4. 很好，你已经很努力了！（注：应鼓励“最佳表现”，而非仅“努力”）"
]
y_pos = 490
for line in negative_lines:
    draw_string(c, 120, y_pos, line, "STSong-Light", 11, RGBColor(51, 51, 51))
    y_pos -= 25

# 5. 页脚
draw_line(c, 100, 60, 500, 60, RGBColor(153, 153, 153), 1)
draw_string(c, 100, 40, "第 12 页", "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 200, 40, "关注“双培强基工程”公众号，获取电子版报告和更多成长建议。", "STSong-Light", 10, RGBColor(102, 102, 102))

c.showPage()  # 结束第12页

# 初始化第13页画布
c = canvas.Canvas("B4-核心认知能力和成长性思维-宫亦涵.pdf", pagesize=A4)
width, height = A4

# 1. 页面标题
draw_string(c, 100, 780, "自驱力测评报告", "STSong-Light", 24, RGBColor(46, 74, 107))
draw_string(c, 100, 755, "SELF DRIVING FORCE REPORT", "Helvetica-Bold", 14, RGBColor(46, 74, 107))

# 2. 个人信息栏
info_col1 = ["姓 名:宫文学", "档案ID:M9822936", "测试时间:2025-07-29"]
info_col2 = ["出生日期:2008-01-08", "指导师:DAN11352", "报告编码:11340869020"]
draw_two_table(c, 100, 720, info_col1, info_col2, 12, RGBColor(51, 51, 51))

# 3. 自驱力定义
draw_string(c, 100, 650, "自驱力 丨 SELF DRIVING FORCE", "STSong-Light", 16, RGBColor(211, 47, 47))
drive_def = "自驱力是个体做某事时自我驱动的能力，它就像汽车的燃油箱，属于车的动力系统。自驱力高低决定了个体参与的积极性和自觉性。日常生活中，个体不爱学习、写作业磨蹭、上课走神等很多问题均在一定程度上和自驱力有关。"
draw_paragraph(c, 100, 620, 400, drive_def, "STSong-Light", 11, RGBColor(51, 51, 51))

# 4. 测评结果详情（三大影响因素）
draw_string(c, 100, 560, "测评结果详情 丨 RESULTS DETAILS", "STSong-Light", 16, RGBColor(211, 47, 47))
factors = [
    "自主性(Autonomy)：这件事是否个体发自内心的决定，是否是他自主的行为；",
    "胜任感(Competence)：个体是否认为他有能力胜任这件事；",
    "归属感(Relatedness)：这件事是否满足个体与人互动，群体归属感的需要。"
]
y_pos = 530
for factor in factors:
    draw_string(c, 120, y_pos, factor, "STSong-Light", 11, RGBColor(51, 51, 51))
    y_pos -= 25

# 5. 发展表现（双列对比）
draw_string(c, 100, 460, "发展表现 丨 DEVELOPMENTAL CHARACTERISTICS", "STSong-Light", 16, RGBColor(211, 47, 47))
high_perf = ["高分表现：", "我可以做我自己，乐意表达想法", "身边人考虑我的感受，对我友好", "我能把事情完成得很好", "常从学习生活中感到成就感", "与家人朋友相处融洽"]
low_perf = ["低分表现：", "我没有太多机会决定自己的事", "常感到有压力，不得不做别人安排的事", "常觉得自己能力不行", "学习生活常让我感到挫败", "没有太多亲近的人，周围人不太喜欢我"]
draw_two_table(c, 100, 430, high_perf, low_perf, 11, RGBColor(51, 51, 51))

# 6. 页脚
draw_line(c, 100, 60, 500, 60, RGBColor(153, 153, 153), 1)
draw_string(c, 100, 40, "第 13 页", "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 200, 40, "关注“双培强基工程”公众号，获取电子版报告和更多成长建议。", "STSong-Light", 10, RGBColor(102, 102, 102))

c.showPage()  # 结束第13页

# 初始化第14页画布


# 初始化第14页画布
c = canvas.Canvas("B4-核心认知能力和成长性思维-宫亦涵.pdf", pagesize=A4)
width, height = A4  # A4尺寸：(595.27, 841.89)

# 1. 页面标题
draw_string(c, 100, 780, "成长建议：发展内驱力", "STSong-Light", 24, RGBColor(46, 74, 107))
draw_string(c, 100, 755, "GROWTH ADVICE: DEVELOP INTERNAL DRIVE", "Helvetica-Bold", 14, RGBColor(46, 74, 107))

# 2. 建议核心引言
intro_text = "你是否因为找不到学习的意义和价值而感到苦恼，是否为能否掌控自己的人生而焦虑？两步帮你了解自己学习内驱力的类型，以及如何在日常学习和生活中掌握自主掌控人生的力量。"
draw_paragraph(c, 100, 720, 400, intro_text, "STSong-Light", 11, RGBColor(51, 51, 51))

# 3. 第一步：内驱力类型与影响（表格呈现）
draw_string(c, 100, 670, "第一步：了解内驱力类型及影响", "STSong-Light", 16, RGBColor(211, 47, 47))
# 内驱力类型表头（含强度、动机类型、原因、影响）
header = ["自驱力强度", "动机类型", "原因", "影响"]
# 内驱力类型数据（匹配文档第2-394段）
drive_data = [
    [
        "无动机", 
        "无能为力，毫无意愿", 
        "被动，躲避，对立的行为", 
        "缺乏安全感，害怕失败，抗拒，冷漠"
    ],
    [
        "被控制的动机（外在）", 
        "外部压力驱动", 
        "因外部压力做事（如避免责骂、为奖励学习）", 
        "紧张、焦虑，很难坚持，缺乏参与，表现不满"
    ],
    [
        "被控制的动机（内在）", 
        "内部压力驱动", 
        "出于内部压力不得不做（如认为学习是职责）", 
        "愧疚感，羞耻感，自我价值感低"
    ],
    [
        "自主的动机（有用驱动）", 
        "受有用性驱动", 
        "为未来做准备（如为更多选择机会而学习）", 
        "意志力，能坚持，但缺乏深层满足感"
    ],
    [
        "自主的动机（价值观驱动）", 
        "价值观驱动", 
        "符合根深蒂固的价值观（如认可学习的意义）", 
        "精力充沛，坚持，深入学习"
    ],
    [
        "自主的动机（内部）", 
        "兴趣驱动", 
        "因有趣或愉快而做事", 
        "快乐，表现良好，满足感强"
    ]
]
# 绘制内驱力类型表格（宽400，高200，适配页面空间）
draw_rect(c, 100, 450, 400, 200, RGBColor(245, 245, 245), RGBColor(153, 153, 153), 1)
# 绘制表头
header_y = 640
for i, h in enumerate(header):
    draw_string(c, 110 + i*90, header_y, h, "STSong-Light", 10, RGBColor(46, 74, 107))
# 绘制数据行
row_y = 620
for row in drive_data:
    for i, cell in enumerate(row):
        # 适配文本长度，分两行显示
        draw_paragraph(c, 110 + i*90, row_y - 10, 80, cell, "STSong-Light", 8, RGBColor(51, 51, 51))
    row_y -= 30

# 4. 第二步：三招发展内驱力（分点呈现）
draw_string(c, 100, 430, "第二步：三招发展内驱力", "STSong-Light", 16, RGBColor(211, 47, 47))
strategies = [
    {
        "title": "“我能决定自己的选择”——给自主选择机会",
        "content": "给孩子提供选择，让他决定做什么、不做什么及时间安排。例如：想培养阅读习惯，让孩子选择感兴趣的主题、类型及阅读时间。"
    },
    {
        "title": "“我能做到”——让孩子感受胜任感",
        "content": "和孩子一起设置合理目标，避免目标过高或过大导致压力与挫败感。长期挫败易让孩子产生无力感，合理目标能逐步建立能力自信。"
    },
    {
        "title": "“我需要”——社会价值观内化",
        "content": "作为社会性个体，需遵守共同规则（如课堂安静、购物排队）。引导孩子理解规则背后的责任与义务，将外部要求转化为内在价值观。"
    }
]
# 绘制策略内容
strat_y = 400
for strat in strategies:
    draw_string(c, 120, strat_y, strat["title"], "STSong-Light", 12, RGBColor(46, 74, 107))
    draw_paragraph(c, 140, strat_y - 20, 360, strat["content"], "STSong-Light", 10, RGBColor(51, 51, 51))
    strat_y -= 60

# 5. 二维码区域（右侧，匹配文档引导）
draw_rect(c, 450, 150, 80, 80, RGBColor(255, 255, 255), RGBColor(153, 153, 153), 1)
draw_string(c, 440, 140, "扫二维码", "STSong-Light", 10, RGBColor(51, 51, 51))
draw_string(c, 420, 125, "保存孩子电子报告观看专家成长建议", "STSong-Light", 8, RGBColor(51, 51, 51))

# 6. 页脚
draw_line(c, 100, 60, 500, 60, RGBColor(153, 153, 153), 1)
draw_string(c, 100, 40, "第 14 页", "STSong-Light", 10, RGBColor(102, 102, 102))
draw_string(c, 200, 40, "关注“双培强基工程”公众号，获取电子版报告和更多成长建议。", "STSong-Light", 10, RGBColor(102, 102, 102))

c.showPage()  # 结束第14页
# 若需生成完整PDF，最后需调用c.save()
# c.save()


c.save()
print(f"PDF created successfully: {filename}")