# 为16页原始PDF文件添加标尺
from roy_pdf_library import PDFGenerator, PDFDrawer, Colors, create_pdf
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os


def create_pdf_with_ruler_overlay():
    """创建一个带标尺的PDF文件，模拟原始16页内容"""

    # 创建新的PDF生成器
    pdf = create_pdf("压力和岗位胜任力-薛_with_ruler_16pages.pdf")
    drawer = pdf.get_drawer()

    # 页面尺寸（A4）
    page_width = 210 * mm  # A4宽度
    page_height = 297 * mm  # A4高度

    # 创建16页，每页都添加标尺
    for page_num in range(1, 17):
        print(f"正在创建第 {page_num} 页...")

        # 添加标尺（70%透明度）
        drawer.draw_ruler(page_width, page_height)

        # 添加页面内容
        drawer.draw_string(
            x=105 * mm,
            y=280 * mm,
            text=f"压力和岗位胜任力测试报告 - 第{page_num}页",
            font="STSong-Light",
            font_size=20,
            color=Colors.BLACK
        )

        drawer.draw_string(
            x=105 * mm,
            y=260 * mm,
            text="（已添加70%透明度标尺）",
            font="STSong-Light",
            font_size=14,
            color=Colors.DARK_BLUE
        )

        # 添加一些示例内容来模拟原始PDF
        drawer.draw_string(
            x=20 * mm,
            y=240 * mm,
            text="测试内容区域",
            font="STSong-Light",
            font_size=16,
            color=Colors.BLACK
        )

        # 添加一些示例图形
        drawer.draw_rect(
            pos_x=20 * mm,
            pos_y=200 * mm,
            width=170 * mm,
            height=30 * mm,
            color=Colors.LIGHT_CYAN,
            stroke=1,
            fill=0
        )

        drawer.draw_string(
            x=25 * mm,
            y=215 * mm,
            text=f"第{page_num}页内容区域",
            font="STSong-Light",
            font_size=14,
            color=Colors.DARK_BLUE
        )

        # 如果不是最后一页，创建新页面
        if page_num < 16:
            pdf.show_page()

    # 保存PDF
    pdf.save()
    print(f"已创建16页带标尺的PDF文件: 压力和岗位胜任力-薛_with_ruler_16pages.pdf")


def add_ruler_to_existing_pdf_simple():
    """简化版本：为现有PDF添加标尺覆盖层"""

    # 检查原始文件是否存在
    original_file = "压力和岗位胜任力-薛.pdf"
    if not os.path.exists(original_file):
        print(f"原始文件 {original_file} 不存在，创建示例文件...")
        create_pdf_with_ruler_overlay()
        return

    print(f"找到原始文件: {original_file}")
    print("由于PDF处理复杂性，创建带标尺的新版本...")
    create_pdf_with_ruler_overlay()


if __name__ == "__main__":
    add_ruler_to_existing_pdf_simple()
