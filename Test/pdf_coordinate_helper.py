#!/usr/bin/env python3
"""
A4 PDF Coordinate Helper

This tool helps convert positions on A4 paper to x,y coordinates for PDF generation.
A4 paper size is 210mm × 297mm (8.27in × 11.69in)
In PDF units (points), A4 is 595 × 842 points (72 points = 1 inch)
"""

import tkinter as tk
from tkinter import ttk
import math

class PDFCoordinateHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Coordinate Helper")
        
        # A4 dimensions in points (72 points = 1 inch)
        self.a4_width = 595
        self.a4_height = 842
        
        # Canvas scale factor (to fit on screen)
        self.scale = 0.8
        
        # Set up the main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create canvas to represent A4 paper
        self.canvas_width = int(self.a4_width * self.scale)
        self.canvas_height = int(self.a4_height * self.scale)
        self.canvas = tk.Canvas(self.main_frame, width=self.canvas_width, height=self.canvas_height, 
                               background="white", bd=1, relief="solid")
        self.canvas.grid(row=0, column=0, padx=10, pady=10)
        
        # Draw grid lines (every 100 points)
        self.draw_grid()
        
        # Info frame for coordinates
        self.info_frame = ttk.LabelFrame(self.main_frame, text="Coordinates", padding="10")
        self.info_frame.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.N, tk.S))
        
        # Coordinate display
        ttk.Label(self.info_frame, text="Click on canvas to get coordinates").grid(row=0, column=0, columnspan=2, pady=5)
        
        ttk.Label(self.info_frame, text="X:").grid(row=1, column=0, sticky=tk.E, pady=2)
        self.x_var = tk.StringVar(value="0")
        ttk.Label(self.info_frame, textvariable=self.x_var).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(self.info_frame, text="Y:").grid(row=2, column=0, sticky=tk.E, pady=2)
        self.y_var = tk.StringVar(value="0")
        ttk.Label(self.info_frame, textvariable=self.y_var).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Manual coordinate entry
        ttk.Separator(self.info_frame, orient="horizontal").grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.E, tk.W))
        
        ttk.Label(self.info_frame, text="Enter coordinates:").grid(row=4, column=0, columnspan=2, pady=5)
        
        ttk.Label(self.info_frame, text="X:").grid(row=5, column=0, sticky=tk.E, pady=2)
        self.x_entry = ttk.Entry(self.info_frame, width=10)
        self.x_entry.grid(row=5, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(self.info_frame, text="Y:").grid(row=6, column=0, sticky=tk.E, pady=2)
        self.y_entry = ttk.Entry(self.info_frame, width=10)
        self.y_entry.grid(row=6, column=1, sticky=tk.W, pady=2)
        
        ttk.Button(self.info_frame, text="Show Point", command=self.show_point).grid(row=7, column=0, columnspan=2, pady=10)
        
        # Reference points
        self.ref_frame = ttk.LabelFrame(self.main_frame, text="Reference Points", padding="10")
        self.ref_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Common positions
        positions = [
            ("Top Left", 50, 792),
            ("Top Center", 297, 792),
            ("Top Right", 545, 792),
            ("Middle Left", 50, 421),
            ("Center", 297, 421),
            ("Middle Right", 545, 421),
            ("Bottom Left", 50, 50),
            ("Bottom Center", 297, 50),
            ("Bottom Right", 545, 50)
        ]
        
        # Create buttons for reference points
        col = 0
        for name, x, y in positions:
            ttk.Button(self.ref_frame, text=name, 
                      command=lambda x=x, y=y: self.highlight_point(x, y)).grid(row=0, column=col, padx=5, pady=5)
            col += 1
        
        # Bind mouse click on canvas
        self.canvas.bind("<Button-1>", self.canvas_click)
        
        # Current point marker
        self.current_point = None
    
    def draw_grid(self):
        # Draw vertical grid lines
        for x in range(0, self.a4_width, 100):
            scaled_x = x * self.scale
            self.canvas.create_line(scaled_x, 0, scaled_x, self.canvas_height, fill="#CCCCCC", dash=(2, 4))
            # Add x-axis labels
            if x > 0:
                self.canvas.create_text(scaled_x, self.canvas_height - 10, text=str(x), fill="#666666", font=("Arial", 8))
        
        # Draw horizontal grid lines
        for y in range(0, self.a4_height, 100):
            scaled_y = y * self.scale
            self.canvas.create_line(0, self.canvas_height - scaled_y, self.canvas_width, self.canvas_height - scaled_y, 
                                   fill="#CCCCCC", dash=(2, 4))
            # Add y-axis labels
            if y > 0:
                self.canvas.create_text(10, self.canvas_height - scaled_y, text=str(y), fill="#666666", font=("Arial", 8))
    
    def canvas_click(self, event):
        # Convert screen coordinates to PDF coordinates
        x = int(event.x / self.scale)
        # Invert y-coordinate (PDF origin is bottom-left)
        y = int((self.canvas_height - event.y) / self.scale)
        
        # Update coordinate display
        self.x_var.set(str(x))
        self.y_var.set(str(y))
        
        # Update entry fields
        self.x_entry.delete(0, tk.END)
        self.x_entry.insert(0, str(x))
        self.y_entry.delete(0, tk.END)
        self.y_entry.insert(0, str(y))
        
        # Highlight the point
        self.highlight_point(x, y)
    
    def show_point(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            self.highlight_point(x, y)
        except ValueError:
            pass
    
    def highlight_point(self, x, y):
        # Remove previous point marker
        if self.current_point:
            self.canvas.delete(self.current_point)
            if hasattr(self, 'current_point_text'):
                self.canvas.delete(self.current_point_text)
        
        # Convert PDF coordinates to screen coordinates
        screen_x = x * self.scale
        # Invert y-coordinate (PDF origin is bottom-left)
        screen_y = self.canvas_height - (y * self.scale)
        
        # Draw new point marker
        self.current_point = self.canvas.create_oval(screen_x-5, screen_y-5, screen_x+5, screen_y+5, 
                                                   fill="red", outline="black")
        self.current_point_text = self.canvas.create_text(screen_x+15, screen_y-15, 
                                                        text=f"({x}, {y})", fill="black")
        
        # Update coordinate display
        self.x_var.set(str(x))
        self.y_var.set(str(y))

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFCoordinateHelper(root)
    root.mainloop()