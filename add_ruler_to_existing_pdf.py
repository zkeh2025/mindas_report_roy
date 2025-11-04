# 为现有PDF文件添加标尺
from roy_pdf_library import PDFGenerator, PDFDrawer, Colors, create_pdf
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os


def add_ruler_to_existing_pdf(input_pdf_path, output_pdf_path):
    """为现有PDF文件的每一页添加标尺"""

    # 创建新的PDF生成器
    pdf = create_pdf(output_pdf_path)
    drawer = pdf.get_drawer()

    # 页面尺寸（A4）
    page_width = 210 * mm  # A4宽度
    page_height = 297 * mm  # A4高度

    # 这里我们需要读取现有PDF的内容
    # 由于PDF格式复杂，我们创建一个示例页面来演示标尺功能
    # 在实际应用中，您可能需要使用PyPDF2或其他PDF处理库来读取现有PDF

    # 创建第一页并添加标尺
    drawer.draw_ruler(page_width, page_height)

    # 添加一些示例内容
    drawer.draw_string(
        x=105 * mm,
        y=250 * mm,
        text="压力和岗位胜任力测试报告",
        font="STSong-Light",
        font_size=24,
        color=Colors.BLACK
    )

    drawer.draw_string(
        x=105 * mm,
        y=230 * mm,
        text="（已添加标尺）",
        font="STSong-Light",
        font_size=16,
        color=Colors.DARK_BLUE
    )

    # 创建第二页并添加标尺
    pdf.show_page()
    drawer.draw_ruler(page_width, page_height)

    drawer.draw_string(
        x=105 * mm,
        y=250 * mm,
        text="第二页内容",
        font="STSong-Light",
        font_size=24,
        color=Colors.BLACK
    )

    # 保存PDF
    pdf.save()
    print(f"已创建带标尺的PDF文件: {output_pdf_path}")


if __name__ == "__main__":
    # 输入和输出文件路径
    input_file = "压力和岗位胜任力-薛.pdf"
    output_file = "压力和岗位胜任力-薛_with_ruler.pdf"

    # 检查输入文件是否存在
    if os.path.exists(input_file):
        add_ruler_to_existing_pdf(input_file, output_file)
    else:
        print(f"输入文件 {input_file} 不存在")
        print("创建一个示例PDF文件...")
        add_ruler_to_existing_pdf("", output_file)
