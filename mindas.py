from fpdf import FPDF

pdf = FPDF()

pdf.add_page()

pdf.set_font("Arial", size=12)
pdf.text(10, 10, text="Hello World!")
pdf.text(10, 20, "this is another line of text.")

pdf.output("simple_pdf.pdf")

print("simple_pdf.pdf successfully created")
