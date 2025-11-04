#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF坐标扫描器
扫描PDF文件并提取所有坐标信息，包括文本、图形和图像的位置
"""

import fitz  # PyMuPDF
import sys
import json
from typing import List, Dict, Any


class PDFCoordinateScanner:
    """PDF坐标扫描器类"""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = None
        self.coordinates = []

    def open_pdf(self):
        """打开PDF文件"""
        try:
            self.doc = fitz.open(self.pdf_path)
            print(f"成功打开PDF文件: {self.pdf_path}")
            print(f"总页数: {len(self.doc)}")
        except Exception as e:
            print(f"打开PDF文件失败: {e}")
            return False
        return True

    def scan_page_coordinates(self, page_num: int) -> Dict[str, Any]:
        """扫描指定页面的所有坐标信息"""
        page = self.doc[page_num]
        page_info = {
            "page_number": page_num + 1,
            "page_size": {
                "width": page.rect.width,
                "height": page.rect.height
            },
            "text_blocks": [],
            "images": [],
            "drawings": [],
            "annotations": []
        }

        # 提取文本块坐标
        text_dict = page.get_text("dict")
        for block in text_dict["blocks"]:
            if "lines" in block:
                block_info = {
                    "type": "text_block",
                    "bbox": block["bbox"],  # [x0, y0, x1, y1]
                    "lines": []
                }

                for line in block["lines"]:
                    line_info = {
                        "bbox": line["bbox"],
                        "spans": []
                    }

                    for span in line["spans"]:
                        span_info = {
                            "bbox": span["bbox"],
                            "text": span["text"],
                            "font": span["font"],
                            "size": span["size"],
                            "color": span["color"]
                        }
                        line_info["spans"].append(span_info)

                    block_info["lines"].append(line_info)

                page_info["text_blocks"].append(block_info)

        # 提取图像坐标
        image_list = page.get_images()
        for img_index, img in enumerate(image_list):
            img_info = {
                "type": "image",
                "index": img_index,
                "xref": img[0],
                "bbox": None  # 需要进一步处理获取实际位置
            }

            # 获取图像在页面中的实际位置
            img_rects = page.get_image_rects(img[0])
            if img_rects:
                img_info["bbox"] = img_rects[0]

            page_info["images"].append(img_info)

        # 提取绘图元素坐标
        drawings = page.get_drawings()
        for drawing in drawings:
            drawing_info = {
                "type": "drawing",
                "items": []
            }

            for item in drawing["items"]:
                item_info = {
                    "type": item[0],
                    "coordinates": item[1:] if len(item) > 1 else []
                }
                drawing_info["items"].append(item_info)

            page_info["drawings"].append(drawing_info)

        # 提取注释坐标
        annotations = page.annots()
        for annot in annotations:
            annot_info = {
                "type": "annotation",
                "bbox": annot.rect,
                "content": annot.content,
                "type_name": annot.type[1] if annot.type else "unknown"
            }
            page_info["annotations"].append(annot_info)

        return page_info

    def scan_all_pages(self):
        """扫描所有页面的坐标信息"""
        if not self.doc:
            print("PDF文件未打开")
            return

        print("开始扫描PDF坐标信息...")

        for page_num in range(len(self.doc)):
            print(f"正在扫描第 {page_num + 1} 页...")
            page_coords = self.scan_page_coordinates(page_num)
            self.coordinates.append(page_coords)

        print("扫描完成!")

    def print_coordinate_summary(self):
        """打印坐标信息摘要"""
        print("\n" + "="*60)
        print("PDF坐标信息摘要")
        print("="*60)

        total_text_blocks = 0
        total_images = 0
        total_drawings = 0
        total_annotations = 0

        for page_info in self.coordinates:
            page_num = page_info["page_number"]
            text_count = len(page_info["text_blocks"])
            image_count = len(page_info["images"])
            drawing_count = len(page_info["drawings"])
            annotation_count = len(page_info["annotations"])

            total_text_blocks += text_count
            total_images += image_count
            total_drawings += drawing_count
            total_annotations += annotation_count

            print(f"\n第 {page_num} 页:")
            print(
                f"  页面尺寸: {page_info['page_size']['width']:.1f} x {page_info['page_size']['height']:.1f}")
            print(f"  文本块: {text_count}")
            print(f"  图像: {image_count}")
            print(f"  绘图元素: {drawing_count}")
            print(f"  注释: {annotation_count}")

        print(f"\n总计:")
        print(f"  文本块: {total_text_blocks}")
        print(f"  图像: {total_images}")
        print(f"  绘图元素: {total_drawings}")
        print(f"  注释: {total_annotations}")

    def print_detailed_coordinates(self):
        """打印详细的坐标信息"""
        print("\n" + "="*60)
        print("详细坐标信息")
        print("="*60)

        for page_info in self.coordinates:
            page_num = page_info["page_number"]
            print(f"\n第 {page_num} 页详细坐标:")
            print("-" * 40)

            # 文本块坐标
            for i, text_block in enumerate(page_info["text_blocks"]):
                print(f"  文本块 {i+1}:")
                print(
                    f"    位置: ({text_block['bbox'][0]:.1f}, {text_block['bbox'][1]:.1f}) - ({text_block['bbox'][2]:.1f}, {text_block['bbox'][3]:.1f})")

                for j, line in enumerate(text_block["lines"]):
                    print(
                        f"    行 {j+1}: ({line['bbox'][0]:.1f}, {line['bbox'][1]:.1f}) - ({line['bbox'][2]:.1f}, {line['bbox'][3]:.1f})")

                    for k, span in enumerate(line["spans"]):
                        text_preview = span["text"][:20] + \
                            "..." if len(span["text"]) > 20 else span["text"]
                        print(
                            f"      文本 {k+1}: ({span['bbox'][0]:.1f}, {span['bbox'][1]:.1f}) - ({span['bbox'][2]:.1f}, {span['bbox'][3]:.1f}) - '{text_preview}'")

            # 图像坐标
            for i, image in enumerate(page_info["images"]):
                print(f"  图像 {i+1}:")
                if image["bbox"]:
                    print(
                        f"    位置: ({image['bbox'][0]:.1f}, {image['bbox'][1]:.1f}) - ({image['bbox'][2]:.1f}, {image['bbox'][3]:.1f})")
                else:
                    print(f"    位置: 无法获取")

            # 绘图元素坐标
            for i, drawing in enumerate(page_info["drawings"]):
                print(f"  绘图元素 {i+1}:")
                for j, item in enumerate(drawing["items"]):
                    print(
                        f"    元素 {j+1}: {item['type']} - 坐标: {item['coordinates']}")

            # 注释坐标
            for i, annotation in enumerate(page_info["annotations"]):
                print(f"  注释 {i+1}:")
                print(
                    f"    位置: ({annotation['bbox'][0]:.1f}, {annotation['bbox'][1]:.1f}) - ({annotation['bbox'][2]:.1f}, {annotation['bbox'][3]:.1f})")
                print(f"    类型: {annotation['type_name']}")
                if annotation["content"]:
                    content_preview = annotation["content"][:50] + "..." if len(
                        annotation["content"]) > 50 else annotation["content"]
                    print(f"    内容: {content_preview}")

    def save_coordinates_to_file(self, output_file: str):
        """将坐标信息保存到文件"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.coordinates, f, ensure_ascii=False, indent=2)
            print(f"坐标信息已保存到: {output_file}")
        except Exception as e:
            print(f"保存文件失败: {e}")

    def close(self):
        """关闭PDF文件"""
        if self.doc:
            self.doc.close()


def main():
    """主函数"""
    pdf_path = "压力和岗位胜任力-薛.pdf"

    # 创建扫描器
    scanner = PDFCoordinateScanner(pdf_path)

    # 打开PDF
    if not scanner.open_pdf():
        return

    try:
        # 扫描所有页面
        scanner.scan_all_pages()

        # 打印摘要
        scanner.print_coordinate_summary()

        # 打印详细坐标
        scanner.print_detailed_coordinates()

        # 保存到文件
        scanner.save_coordinates_to_file("pdf_coordinates.json")

    finally:
        # 关闭PDF
        scanner.close()


if __name__ == "__main__":
    main()
