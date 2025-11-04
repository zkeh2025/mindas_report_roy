# 迁移指南：从 reportlab_v1.py 到 roy_pdf_library.py

## 概述

本指南将帮助您将现有的 `reportlab_v1.py` 代码迁移到新的自定义库 `roy_pdf_library.py`。

## 主要变化

### 1. 导入方式变化

**原始代码：**
```python
from reportlab.pdfgen import canvas
c = canvas.Canvas("output.pdf")
```

**新库方式：**
```python
from roy_pdf_library import create_pdf, Colors
pdf = create_pdf("output.pdf")
drawer = pdf.get_drawer()
```

### 2. 函数调用方式变化

**原始代码：**
```python
draw_string(c, 100, 700, text="Hello", font_size=20)
draw_rect(c, pos_x=50, pos_y=600, width=100, height=50)
```

**新库方式：**
```python
drawer.draw_string(100, 700, text="Hello", font_size=20)
drawer.draw_rect(pos_x=50, pos_y=600, width=100, height=50)
```

### 3. 颜色使用变化

**原始代码：**
```python
cyan = [0.17255, 0.67059, 0.69804]
draw_string(c, 100, 700, text="Hello", color=cyan)
```

**新库方式：**
```python
from roy_pdf_library import Colors
drawer.draw_string(100, 700, text="Hello", color=Colors.CYAN)
```

## 详细迁移步骤

### 步骤1：更新导入语句

将文件顶部的导入语句替换为：

```python
from roy_pdf_library import create_pdf, Colors
```

### 步骤2：创建PDF生成器

将：
```python
c = canvas.Canvas("filename.pdf")
```

替换为：
```python
pdf = create_pdf("filename.pdf")
drawer = pdf.get_drawer()
```

### 步骤3：更新函数调用

将所有函数调用从：
```python
function_name(c, ...)
```

改为：
```python
drawer.function_name(...)
```

### 步骤4：更新颜色引用

将颜色变量替换为预定义常量：

| 原始变量 | 新常量 |
|---------|--------|
| `cyan` | `Colors.CYAN` |
| `darkercyan` | `Colors.DARKER_CYAN` |
| `black` | `Colors.BLACK` |
| `lightcyan` | `Colors.LIGHT_CYAN` |
| `red` | `Colors.RED` |
| `lightpurple` | `Colors.LIGHT_PURPLE` |
| `orange` | `Colors.ORANGE` |
| `darkblue` | `Colors.DARK_BLUE` |
| `green` | `Colors.GREEN` |
| `white_color` | `Colors.WHITE` |

### 步骤5：更新保存方式

将：
```python
c.save()
```

替换为：
```python
pdf.save()
```

## 完整迁移示例

### 原始代码片段：
```python
from reportlab.pdfgen import canvas

c = canvas.Canvas("output.pdf")

cyan = [0.17255, 0.67059, 0.69804]
draw_string(c, 100, 700, text="Hello", color=cyan)
draw_rect(c, pos_x=50, pos_y=600, width=100, height=50, color=cyan)

c.save()
```

### 迁移后的代码：
```python
from roy_pdf_library import create_pdf, Colors

pdf = create_pdf("output.pdf")
drawer = pdf.get_drawer()

drawer.draw_string(100, 700, text="Hello", color=Colors.CYAN)
drawer.draw_rect(pos_x=50, pos_y=600, width=100, height=50, color=Colors.CYAN)

pdf.save()
```

## 函数映射表

| 原始函数 | 新库方法 | 说明 |
|---------|---------|------|
| `draw_string(c, ...)` | `drawer.draw_string(...)` | 绘制文本 |
| `draw_string_vertically_centered(c, ...)` | `drawer.draw_string_vertically_centered(...)` | 绘制垂直居中文本 |
| `upload_image(c, ...)` | `drawer.upload_image(...)` | 上传图像 |
| `draw_bulltin(...)` | `drawer.draw_bulletin(...)` | 绘制项目符号 |
| `draw_line(...)` | `drawer.draw_line(...)` | 绘制直线 |
| `draw_string_list(...)` | `drawer.draw_string_list(...)` | 绘制文本列表 |
| `draw_rect(...)` | `drawer.draw_rect(...)` | 绘制矩形 |
| `draw_dotted_line(...)` | `drawer.draw_dotted_line(...)` | 绘制虚线 |
| `draw_cut_rectangle(c, ...)` | `drawer.draw_cut_rectangle(...)` | 绘制切角矩形 |
| `draw_rounded_rect_one_corner(...)` | `drawer.draw_rounded_rect_one_corner(...)` | 绘制单角圆角矩形 |
| `draw_cognitive_domain(...)` | `drawer.draw_cognitive_domain(...)` | 绘制认知领域 |
| `draw_two_table(c, ...)` | `drawer.draw_two_table(...)` | 绘制两列表格 |

## 注意事项

1. **参数顺序**：大部分函数的参数顺序保持不变，只是移除了第一个 `c` 参数
2. **默认值**：所有默认值都保持不变
3. **返回值**：函数行为保持一致
4. **错误处理**：新库包含相同的错误处理逻辑

## 测试迁移

迁移完成后，建议运行以下代码测试：

```python
from roy_pdf_library import create_pdf, Colors

# 创建测试PDF
pdf = create_pdf("test_migration.pdf")
drawer = pdf.get_drawer()

# 测试基本功能
drawer.draw_string(100, 700, text="迁移测试", font_size=20)
drawer.draw_rect(50, 600, width=100, height=50, color=Colors.CYAN)
drawer.draw_line(50, 500, 200, 500, width=2, color=Colors.RED)

# 保存并检查结果
pdf.save()
print("迁移测试完成！")
```

## 常见问题

**Q: 为什么需要迁移？**
A: 新库提供了更好的代码组织、类型安全和可维护性。

**Q: 迁移后性能有影响吗？**
A: 性能基本没有影响，新库只是对原始函数的封装。

**Q: 可以逐步迁移吗？**
A: 可以，您可以先迁移部分代码，逐步完成整个项目的迁移。

**Q: 原始代码还能用吗？**
A: 原始代码仍然可以正常使用，但建议迁移到新库以获得更好的开发体验。

