# 将标尺叠加到员工抗压力和岗位胜任力报告PDF上
# This script overlays a ruler onto the existing PDF report

# Import system modules
from roy_pdf_library import PDFGenerator, PDFDrawer, Colors, create_pdf
import PyPDF2
from reportlab.pdfgen import canvas  # canvas = the drawing surface for PDF
from reportlab.lib.pagesizes import A4  # A4 = standard paper size
from reportlab.lib.units import mm  # mm = millimeter units for measurements
import sys
import os
import io

# Add parent directory to path to import roy_pdf_library
# This tells Python to look in the parent folder for our custom library
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# Import reportlab modules for PDF creation

# Import PyPDF2 for merging PDFs
# PyPDF2 = a library that can read existing PDFs and combine them

# Import roy's custom PDF library


def create_ruler_overlay(page_width, page_height):
    """
    创建标尺覆盖层
    Create a ruler overlay layer

    This function creates a transparent ruler grid that we can overlay on the PDF

    Parameters:
    - page_width: The width of the page in points
    - page_height: The height of the page in points

    Returns:
    - PDF data as bytes that can be merged with another PDF
    """
    # 创建内存中的PDF
    # Create a PDF in memory (not saved to disk yet)
    # BytesIO = a memory buffer that acts like a file
    buffer = io.BytesIO()

    # Create a canvas (drawing surface) that draws to the memory buffer
    # canvas.Canvas = the tool we use to draw on the PDF
    c = canvas.Canvas(buffer, pagesize=A4)

    # 创建PDFDrawer对象
    # Create a PDFDrawer object to use our custom drawing functions
    drawer = PDFDrawer(c)

    # 添加标尺（30%透明度）
    # Add ruler with 30% opacity (70% transparent)
    # This draws the grid lines and numbers on the page
    drawer.draw_ruler(page_width, page_height)

    # 完成页面
    # Finish this page
    # showPage() = tells the canvas we're done with this page
    c.showPage()

    # 保存到内存
    # Save to memory buffer
    c.save()

    # 获取PDF数据
    # Get the PDF data from the buffer
    # seek(0) = move to the beginning of the buffer
    buffer.seek(0)

    # Return the PDF data as bytes
    return buffer.getvalue()


def merge_pdf_with_ruler(original_pdf_path, output_pdf_path):
    """
    将标尺叠加到原始PDF上
    Overlay ruler onto the original PDF

    This function:
    1. Reads the original PDF file
    2. Creates a ruler overlay for each page
    3. Merges the ruler with each page
    4. Saves the result to a new PDF file

    Parameters:
    - original_pdf_path: Path to the original PDF file
    - output_pdf_path: Path where the new PDF will be saved

    Returns:
    - True if successful, False if there was an error
    """
    # 检查原始文件是否存在
    # Check if the original file exists
    # os.path.exists() = checks if a file is on the disk
    if not os.path.exists(original_pdf_path):
        print(f"原始文件 {original_pdf_path} 不存在")
        print(f"Original file {original_pdf_path} does not exist")
        return False

    try:
        # 读取原始PDF
        # Read the original PDF file
        # 'rb' = read in binary mode (PDFs are binary files)
        with open(original_pdf_path, 'rb') as original_file:
            # PdfReader = reads PDF files and lets us access their pages
            original_pdf = PyPDF2.PdfReader(original_file)

            # Get the number of pages in the PDF
            num_pages = len(original_pdf.pages)
            print(f"原始PDF有 {num_pages} 页")
            print(f"Original PDF has {num_pages} pages")

            # 创建输出PDF写入器
            # Create a PDF writer to create the new PDF
            # PdfWriter = creates new PDF files
            output_pdf = PyPDF2.PdfWriter()

            # 页面尺寸（A4）
            # Page dimensions (A4 size)
            # A4 width in points (mm converts to points)
            page_width = 210 * mm
            page_height = 297 * mm  # A4 height in points

            # 为每一页添加标尺覆盖层
            # Add ruler overlay to each page
            # range(num_pages) = loops from 0 to num_pages-1
            for page_num in range(num_pages):
                print(f"正在处理第 {page_num + 1} 页...")
                print(f"Processing page {page_num + 1}...")

                # 获取原始页面
                # Get the original page
                original_page = original_pdf.pages[page_num]

                # 创建标尺覆盖层
                # Create the ruler overlay for this page
                ruler_overlay_data = create_ruler_overlay(
                    page_width, page_height)

                # Convert the ruler data back into a PDF that can be read
                # BytesIO wraps the data so PyPDF2 can read it
                ruler_overlay = PyPDF2.PdfReader(
                    io.BytesIO(ruler_overlay_data))
                ruler_page = ruler_overlay.pages[0]

                # 合并原始页面和标尺覆盖层
                # Merge the original page with the ruler overlay
                # merge_page() = puts the ruler on top of the original content
                original_page.merge_page(ruler_page)

                # 添加到输出PDF
                # Add the merged page to the output PDF
                output_pdf.add_page(original_page)

            # 保存合并后的PDF
            # Save the merged PDF to disk
            # 'wb' = write in binary mode
            with open(output_pdf_path, 'wb') as output_file:
                output_pdf.write(output_file)

            print(f"成功创建带标尺的PDF: {output_pdf_path}")
            print(f"Successfully created PDF with ruler: {output_pdf_path}")
            return True

    except Exception as e:
        # If anything goes wrong, print the error
        # Exception = any kind of error
        # str(e) = converts the error to a readable string
        print(f"处理PDF时出错: {str(e)}")
        print(f"Error processing PDF: {str(e)}")
        return False


# Main execution section
# This runs when you execute the script
if __name__ == "__main__":
    # Define the input and output file paths
    # The original PDF we want to add rulers to
    original_file = "员工抗压力和岗位胜任力报告1103.pdf"

    # The new PDF file that will have rulers
    output_file = "员工抗压力和岗位胜任力报告1103_with_ruler.pdf"

    print("="*60)
    print("开始将标尺叠加到PDF上...")
    print("Starting to overlay ruler onto PDF...")
    print("="*60)

    # Call the function to merge the PDF with ruler
    success = merge_pdf_with_ruler(original_file, output_file)

    if success:
        print("\n" + "="*60)
        print("完成！已创建新的PDF文件")
        print("Done! New PDF file created")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("处理失败")
        print("Processing failed")
        print("="*60)
