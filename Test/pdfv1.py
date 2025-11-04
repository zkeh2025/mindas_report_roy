from fpdf import FPDF

# create a pdf that is portriate oriented and uses mm as distance gauge
pdf = FPDF(orientation="p", unit="mm", format="A4")
pdf.set_auto_page_break(auto=False)
pdf.add_page()

# set title font to large and bold


def set_title_font(pdf):
    pdf.set_font("helvetica", style="B", size=16)
    pdf.set_text_color(0, 0, 0)

# set subtitle font as medium size


def set_subtitle_font(pdf):
    pdf.set_font("helvetica", style="B", size=12)
    pdf.set_text_color(0, 20, 0)

# set normal font as small and colour as random


def set_text_font(pdf):
    pdf.set_font("helvetica", style='B', size=10)
    pdf.set_color(60, 60, 60)


set_title_font(pdf)
pdf.text(150, 20, text="Roy")

pdf.output("pdfv1.pdf")
