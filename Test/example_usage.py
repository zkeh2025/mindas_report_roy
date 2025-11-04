# Roy's PDF Library 使用示例

from roy_pdf_library import create_pdf, Colors


def example_usage():
    """示例：如何使用Roy的PDF库"""

    # 创建PDF生成器
    pdf = create_pdf("example_output.pdf")
    drawer = pdf.get_drawer()

    # 1. 绘制文本
    drawer.draw_string(100, 700, text="欢迎使用Roy的PDF库!",
                       font="STSong-Light", font_size=20,
                       color=Colors.DARK_BLUE)

    # 2. 绘制垂直居中的文本
    drawer.draw_string_vertically_centered(200, 650, "垂直居中文本",
                                           font="STSong-Light", font_size=16,
                                           color=Colors.RED)

    # 3. 绘制矩形
    drawer.draw_rect(pos_x=50, pos_y=600, width=100, height=50,
                     radius=5, color=Colors.CYAN, stroke=1, fill=1)

    # 4. 绘制线条
    drawer.draw_line(50, 550, 200, 550, width=2, color=Colors.ORANGE)

    # 5. 绘制虚线
    drawer.draw_dotted_line(50, 500, 200, 500, width=1,
                            color=Colors.GREEN, dash=[4, 2])

    # 6. 绘制项目符号列表
    evaluation_items = ["推理能力", "空间能力", "加工速度", "自我概念"]
    drawer.draw_bulletin(evaluation_content=evaluation_items,
                         y_start=450, x_start=50, font_size=14)

    # 7. 绘制切角矩形
    drawer.draw_cut_rectangle(50, 350, 100, 80, 10)

    # 8. 绘制圆角矩形（单角）
    drawer.draw_rounded_rect_one_corner(200, 350, 80, 100, 15,
                                        stroke_color=Colors.DARK_BLUE,
                                        fill_color=Colors.LIGHT_PURPLE)

    # 9. 绘制认知领域（示例）
    drawer.draw_cognitive_domain(3, 20, "感知觉", "Perception",
                                 "感知是认知、理解的基础。", "98",
                                 is_left_column=True)

    # 10. 绘制表格
    table_data = [
        ["姓", "", "", "名", "：", "张三"],
        ["年", "", "", "龄", "：", "18岁"],
    ]
    drawer.draw_two_table(1.4, 15, table_data)

    # 保存PDF
    pdf.save()
    print("示例PDF已创建: example_output.pdf")


def recreate_original_pdf():
    """重新创建原始PDF的部分内容"""

    pdf = create_pdf("recreated_reportlab_v1.pdf")
    drawer = pdf.get_drawer()

    # 绘制B4矩形
    drawer.draw_rect(pos_x=62, pos_y=712, width=40, height=60,
                     radius=5, color=Colors.DARKER_CYAN)

    # B4文本
    drawer.draw_string(x=80, y=740, text="B4", color=Colors.BLACK)

    # B4线条
    drawer.draw_line(155, 710, 595, 710, color=Colors.DARKER_CYAN)
    drawer.draw_line(155, 799, 600, 799, color=Colors.DARKER_CYAN)

    # 绘制测评内容
    drawer.draw_bulletin(
        y_start=150,
        x_start=20,
        r=3,
        x_cen=-18.5,
        y_decrement=20,
        y_circle_start=152,
        linewidth=0.5,
        font_size=17
    )

    # 绘制标题
    drawer.draw_string(60, 650, font="STSong-Light", font_size=25,
                       color=Colors.LIGHT_CYAN, text="分析型测评包")
    drawer.draw_string(60, 600, font="STSong-Light", font_size=40,
                       color=Colors.LIGHT_CYAN, text="核心认知能力和")
    drawer.draw_string(60, 550, font="STSong-Light", font_size=40,
                       color=Colors.LIGHT_CYAN, text="成长型思维")

    # 绘制测评内容矩形
    drawer.draw_rect(60, 500, width=40, height=11,
                     color=Colors.LIGHT_CYAN, radius=1, fill=True)
    drawer.draw_string(70, 510, font="STSong-Light",
                       font_size=23, color=Colors.WHITE, text="测评内容")

    # 绘制"发现自己"和"点亮未来"
    list_items = ["发", "现", "自", "己"]
    x = 15
    for item in list_items:
        i = (int(list_items.index(item) + 1))
        drawer.draw_string(20 + i * 12 * 2.834645669, 60,
                           font="STSong-Light", font_size=x,
                           color=Colors.BLACK, text=item)

    list_items2 = ["点", "亮", "未", "来"]
    for item in list_items2:
        i = (int(list_items2.index(item) + 1))
        drawer.draw_string(180 + i * 12 * 2.834645669, 60,
                           font="STSong-Light", font_size=x,
                           color=Colors.BLACK, text=item)

    pdf.show_page()
    pdf.save()
    print("重新创建的PDF已保存: recreated_reportlab_v1.pdf")


if __name__ == "__main__":
    print("运行Roy PDF库示例...")
    example_usage()
    print("\n重新创建原始PDF...")
    recreate_original_pdf()
    print("\n所有示例完成！")
