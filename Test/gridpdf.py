from fpdf import FPDF

pdf=FPDF(orientation="p", unit="mm", format="A4")
pdf.add_page()

pdf.set_draw_color(200,200,200)

for y in range (0,300,10):
    pdf.line(x1=0, y1=y, x2=210, y2=y)
    pdf.set_font(family ="helvetica", size=7)
    pdf.text(x=1, y=y+3, text=str(y))


for x in range (0,210,6):
    pdf.line(x1=x, y1=0, x2=x, y2=300)
    pdf.set_font(family ="helvetica", size=7)
    pdf.text(y=3, x=x+3, text=str(x))

pdf.output("gridpdf.pdf")