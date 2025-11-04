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







draw_string(c, 150, 800, "B4 少年 心知 DAN成长计划", "STSong-Light", 16, RGBColor(46, 74, 107))
draw_string(c, 150, 780, "PSYCHDREAM YOUNG", "Helvetica-Bold", 12, RGBColor(46, 74, 107))

c.showPage()
c.save()