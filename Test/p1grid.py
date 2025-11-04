
import pikepdf
from pikepdf import Pdf, Page, Array, Name, Dictionary


def overlay_pdfs_with_transparency(bottom_pdf_path, top_pdf_path, output_pdf_path, opacity):
    with Pdf.open(bottom_pdf_path) as bottom_pdf, Pdf.open(top_pdf_path) as top_pdf:
        output_pdf = Pdf.new()

        min_pages = min(len(bottom_pdf.pages), len(top_pdf.pages))
        if min_pages == 0:
            raise ValueError("One of the PDFs has no pages")
        
        for i in range(min_pages):
            bottom_page = bottom_pdf.pages[i]
            top_page = top_pdf.pages[i]
            bottom_media_box = bottom_page.mediabox
            top_page.mediabox = bottom_media_box

            transparency_dict = Dictionary()

            transparency_dict[Name.BM] = Name.Normal
            transparency_dict[Name.CA] = opacity
            transparency_dict[Name.ca] = opacity 

            if Name.Resource not in top_page:
                top_page[Name.Resource] = Dictionary()

            top_page.Resource.ExtGState = transparency_dict


            original_content = top_page.Contents
            if original_content is None:
                original_content = b""
            else: 
                original_content = original_content.read_bytes()
                
            transparent_content = b"/TransparentState gs\n" + original_content

            top_page.Contents = top_pdf.make_stream(transparent_content)

            merged_page = output_pdf.add_blank_page(
                width=bottom_media_box[2],
                height=bottom_media_box[3]
            )
            merged_page.add_overlay(bottom_page)
            merged_page.add_overlay(top_page)

        output_pdf.save(output_pdf_path)
        print(f"Transparent PDF saved to {output_pdf_path} (Top opacity: {opacity})")
        #add top pdf name and bottom pdf name to print, make them a veriable automatically retrieved instead of needing to manually change code


if __name__ == "__main__": 
    BOTTOM_PDF_PATH = '/Users/Roy/Desktop/mindas-report/TRAE mindas/gridpdf.pdf'
    TOP_PDF_PATH = "/Users/Roy/Desktop/mindas-report/TRAE mindas/P1.pdf"
    OUTPUT_PDF_PATH = "/Users/Roy/Desktop/mindas-report/TRAE mindas/output.pdf"
    OPACITY = 0.5

    overlay_pdfs_with_transparency(BOTTOM_PDF_PATH, TOP_PDF_PATH, OUTPUT_PDF_PATH, OPACITY)



