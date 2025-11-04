# Roy's PDF Library

这是一个基于ReportLab的自定义PDF生成库，包含了从`reportlab_v1.py`中提取的所有绘图和文本处理函数。

## 功能特性

- 🎨 **丰富的绘图功能**：支持文本、矩形、线条、图像等绘制
- 🎯 **精确的定位**：提供垂直居中、坐标定位等功能
- 🌈 **预定义颜色**：包含常用的颜色常量
- 📊 **表格支持**：支持创建各种表格
- 🔤 **中文支持**：内置中文字体支持
- 📝 **项目符号**：支持绘制带编号的项目列表

## 安装依赖

```bash
pip install reportlab pillow
```

## 快速开始

### 基本使用

```python
from roy_pdf_library import create_pdf, Colors

# 创建PDF生成器
pdf = create_pdf("my_document.pdf")
drawer = pdf.get_drawer()

# 绘制文本
drawer.draw_string(100, 700, text="Hello World!", font_size=20)

# 绘制矩形
drawer.draw_rect(50, 600, width=100, height=50, color=Colors.BLUE)

# 保存PDF
pdf.save()
```

### 使用预定义颜色

```python
from roy_pdf_library import Colors

# 可用的颜色常量
Colors.CYAN          # 青色
Colors.DARK_BLUE     # 深蓝色
Colors.RED           # 红色
Colors.ORANGE        # 橙色
Colors.GREEN         # 绿色
Colors.BLACK         # 黑色
Colors.WHITE         # 白色
# ... 更多颜色
```

## API 参考

### PDFGenerator 类

主要的PDF生成器类。

#### 方法

- `__init__(filename)`: 初始化PDF生成器
- `save()`: 保存PDF文件
- `show_page()`: 创建新页面
- `get_canvas()`: 获取ReportLab Canvas对象
- `get_drawer()`: 获取PDFDrawer对象

### PDFDrawer 类

PDF绘图工具类，包含所有绘图方法。

#### 文本绘制

- `draw_string(x, y, text, font, font_size, color)`: 绘制普通文本
- `draw_string_vertically_centered(x, y, text, font, font_size, color)`: 绘制垂直居中文本
- `draw_string_list(x, y, label_list, text_list, ...)`: 绘制文本列表

#### 图形绘制

- `draw_rect(pos_x, pos_y, width, height, radius, color, stroke, fill)`: 绘制矩形
- `draw_line(x1, y1, x2, y2, width, color)`: 绘制直线
- `draw_dotted_line(x1, y1, x2, y2, width, color, dash, alpha)`: 绘制虚线
- `draw_cut_rectangle(x, y, height, width, corner)`: 绘制切角矩形
- `draw_rounded_rect_one_corner(x, y, width, height, corner_radius, stroke_color, fill_color)`: 绘制单角圆角矩形

#### 特殊功能

- `upload_image(image, x, y, width, height, mask)`: 上传并绘制图像
- `draw_bulletin(evaluation_content, y_start, x_start, ...)`: 绘制项目符号列表
- `draw_cognitive_domain(x, y, chinese_name, english_name, description, percentile, is_left_column)`: 绘制认知领域
- `draw_two_table(x, y, data)`: 绘制两列表格

## 使用示例

### 示例1：创建简单文档

```python
from roy_pdf_library import create_pdf, Colors

pdf = create_pdf("simple_doc.pdf")
drawer = pdf.get_drawer()

# 添加标题
drawer.draw_string(100, 750, text="我的文档", 
                  font="STSong-Light", font_size=24, color=Colors.DARK_BLUE)

# 添加内容
drawer.draw_string(50, 700, text="这是第一段内容", font_size=14)

# 添加装饰性矩形
drawer.draw_rect(40, 650, width=200, height=30, 
               color=Colors.LIGHT_CYAN, radius=5)

pdf.save()
```

### 示例2：创建报告页面

```python
from roy_pdf_library import create_pdf, Colors

pdf = create_pdf("report.pdf")
drawer = pdf.get_drawer()

# 绘制标题
drawer.draw_string_vertically_centered(100, 700, "认知能力报告", 
                                     font="STSong-Light", font_size=20, 
                                     color=Colors.DARK_BLUE)

# 绘制项目列表
items = ["推理能力", "空间能力", "加工速度", "注意力", "记忆力"]
drawer.draw_bulletin(evaluation_content=items, y_start=600, x_start=50)

# 绘制分隔线
drawer.draw_line(50, 500, 200, 500, width=1, color=Colors.CYAN)

pdf.save()
```

### 示例3：使用表格

```python
from roy_pdf_library import create_pdf

pdf = create_pdf("table_example.pdf")
drawer = pdf.get_drawer()

# 创建表格数据
data = [
    ["姓", "", "", "名", "：", "张三"],
    ["年", "", "", "龄", "：", "18岁"],
    ["学", "", "", "校", "：", "某某大学"],
]

# 绘制表格
drawer.draw_two_table(1.4, 25, data)

pdf.save()
```

## 从原始代码迁移

如果你有使用原始`reportlab_v1.py`的代码，可以按以下方式迁移：

### 原始代码
```python
# 原始方式
c = canvas.Canvas("output.pdf")
draw_string(c, 100, 700, text="Hello")
c.save()
```

### 新库方式
```python
# 使用新库
from roy_pdf_library import create_pdf

pdf = create_pdf("output.pdf")
drawer = pdf.get_drawer()
drawer.draw_string(100, 700, text="Hello")
pdf.save()
```

## 注意事项

1. **坐标系统**：使用ReportLab的标准坐标系统（左下角为原点）
2. **单位**：默认使用点（point）作为单位，可通过`mm`和`cm`常量转换
3. **字体**：库已自动注册中文字体"STSong-Light"
4. **颜色**：建议使用预定义的`Colors`常量，确保颜色一致性

## 文件结构

```
roy_pdf_library.py    # 主库文件
example_usage.py      # 使用示例
README.md             # 说明文档
```

## 许可证

此库基于原始`reportlab_v1.py`代码创建，请遵循相应的使用条款。
