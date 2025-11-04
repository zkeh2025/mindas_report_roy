# 重新生成595.2 x 960 pts格式的PDF文件（30%透明度标尺）
from roy_pdf_library import PDFGenerator, PDFDrawer, Colors, create_pdf
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import PyPDF2
import io
import os


def create_ruler_overlay_595x960_30percent():
    """创建595.2 x 960 pts格式的标尺覆盖层（30%透明度）"""
    # 创建内存中的PDF
    buffer = io.BytesIO()

    # 使用自定义页面尺寸
    custom_size = (595.2, 960)  # 595.2 x 960 pts
    c = canvas.Canvas(buffer, pagesize=custom_size)

    # 创建PDFDrawer对象
    drawer = PDFDrawer(c)

    # 页面尺寸（pts）
    page_width = 595.2
    page_height = 960

    # 添加标尺（30%透明度）
    # 使用pts单位绘制标尺
    for x in range(0, int(page_width), 20):  # 每20pts一个刻度
        x_pos = x
        # 绘制垂直刻度线覆盖整个页面高度
        drawer.draw_line(x_pos, 0, x_pos, page_height,
                         width=0.5, color=Colors.BLACK, alpha=0.3)
        # 绘制数字标签
        drawer.draw_string(x_pos + 1, 1, text=str(x),
                           font_size=8, color=Colors.BLACK)

    # Y轴标尺（覆盖整个页面高度）
    for y in range(0, int(page_height), 20):  # 每20pts一个刻度
        y_pos = y
        # 绘制水平刻度线覆盖整个页面宽度
        drawer.draw_line(0, y_pos, page_width, y_pos,
                         width=0.5, color=Colors.BLACK, alpha=0.3)
        # 绘制数字标签
        drawer.draw_string(1, y_pos + 1, text=str(y),
                           font_size=8, color=Colors.BLACK)

    # 完成页面
    c.showPage()
    c.save()

    # 获取PDF数据
    buffer.seek(0)
    return buffer.getvalue()


def merge_pdf_with_ruler_595x960_30percent(original_pdf_path, output_pdf_path):
    """将595.2 x 960 pts格式的标尺叠加到原始PDF上（30%透明度）"""

    if not os.path.exists(original_pdf_path):
        print(f"原始文件 {original_pdf_path} 不存在")
        return False

    try:
        # 读取原始PDF
        with open(original_pdf_path, 'rb') as original_file:
            original_pdf = PyPDF2.PdfReader(original_file)
            num_pages = len(original_pdf.pages)
            print(f"原始PDF有 {num_pages} 页")

            # 创建输出PDF写入器
            output_pdf = PyPDF2.PdfWriter()

            # 为每一页添加标尺覆盖层
            for page_num in range(num_pages):
                print(f"正在处理第 {page_num + 1} 页...")

                # 获取原始页面
                original_page = original_pdf.pages[page_num]

                # 创建标尺覆盖层
                ruler_overlay_data = create_ruler_overlay_595x960_30percent()
                ruler_overlay = PyPDF2.PdfReader(
                    io.BytesIO(ruler_overlay_data))
                ruler_page = ruler_overlay.pages[0]

                # 合并原始页面和标尺覆盖层
                original_page.merge_page(ruler_page)

                # 添加到输出PDF
                output_pdf.add_page(original_page)

            # 保存合并后的PDF
            with open(output_pdf_path, 'wb') as output_file:
                output_pdf.write(output_file)

            print(f"成功创建带30%透明度标尺的PDF: {output_pdf_path}")
            return True

    except Exception as e:
        print(f"处理PDF时出错: {str(e)}")
        return False


if __name__ == "__main__":
    original_file = "压力和岗位胜任力-薛.pdf"
    output_file = "压力和岗位胜任力-薛_with_ruler_595x960_30percent.pdf"

    # 尝试使用PyPDF2合并
    print("尝试将595.2 x 960 pts格式的标尺叠加到原始PDF上（30%透明度）...")
    success = merge_pdf_with_ruler_595x960_30percent(
        original_file, output_file)

    if not success:
        print("PyPDF2方法失败")
