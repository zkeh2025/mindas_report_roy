from fpdf import FPDF

# create a pdf that is portriate oriented and uses mm as distance gauge
pdf = FPDF(orientation="p", unit="mm", format="A4")
pdf.set_auto_page_break(auto=False)
pdf.add_page()
pdf.add_font("smiley_sans", "", "smiley.ttf")
# set title font to large and bold
pdf.set_font("smiley_sans",'', size=40)


pdf.set_fill_color(48, 149, 129)
pdf.rect(20, 0, 30, 30, round_corners = ("BOTTOM_RIGHT", "BOTTOM_LEFT"), style = "F")
pdf.cell(20, 20)
pdf.set_text_color(255,255,255)
pdf.cell(10,20, "B4", align="C")


pdf.output("pdfv2.pdf")
