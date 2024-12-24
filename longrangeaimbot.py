import torch
import numpy as np
import cv2
import time
import win32api
import win32con
import pyautogui
import warnings
from PIL import ImageGrab
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

warnings.filterwarnings('ignore', category=FutureWarning)

class CheatMenu:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.window = ctk.CTk()
        self.window.title("Long Range Aimbot Pro")
        self.window.geometry("1000x600")
        self.window.attributes('-topmost', True)
        self.window.resizable(False, False)

        # Create main container with left and right sections
        self.main_container = ctk.CTkFrame(self.window)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left section for main content
        self.left_section = ctk.CTkFrame(self.main_container, width=700)
        self.left_section.pack(side="left", fill="both", expand=True, padx=(0,10))

        # Right section for tab boxes
        self.right_section = ctk.CTkFrame(self.main_container, width=250)
        self.right_section.pack(side="right", fill="y", padx=(10,0))

        # Create tab boxes on right
        self.create_tab_boxes()

        # Create main content area
        self.create_main_content()

        # Initialize variables
        self.is_enabled = False
        self.update_fps = 60
        self.smooth_factor = 0.6
        self.conf_threshold = 0.25
        self.box_size = 100

    def create_tab_boxes(self):
        # Status Box
        self.status_box = ctk.CTkFrame(self.right_section)
        self.status_box.pack(fill="x", pady=(0,10), padx=5)
        
        status_label = ctk.CTkLabel(self.status_box, text="STATUS", font=("Roboto", 16, "bold"))
        status_label.pack(pady=5)
        
        self.enabled = ctk.CTkSwitch(self.status_box, text="Enable Aimbot", command=self.toggle_aimbot)
        self.enabled.pack(pady=5)

        self.fps_label = ctk.CTkLabel(self.status_box, text="FPS: 60")
        self.fps_label.pack(pady=5)

        # Performance Box  
        self.perf_box = ctk.CTkFrame(self.right_section)
        self.perf_box.pack(fill="x", pady=10, padx=5)

        perf_label = ctk.CTkLabel(self.perf_box, text="PERFORMANCE", font=("Roboto", 16, "bold"))
        perf_label.pack(pady=5)

        self.update_rate = ctk.CTkSlider(self.perf_box, from_=1, to=144, command=self.update_rate_value)
        self.update_rate.set(60)
        self.update_rate.pack(pady=5)
        self.update_rate_label = ctk.CTkLabel(self.perf_box, text="Update Rate: 60 FPS")
        self.update_rate_label.pack()

        # Settings Box
        self.settings_box = ctk.CTkFrame(self.right_section) 
        self.settings_box.pack(fill="x", pady=10, padx=5)

        settings_label = ctk.CTkLabel(self.settings_box, text="SETTINGS", font=("Roboto", 16, "bold"))
        settings_label.pack(pady=5)

        self.smoothing = ctk.CTkSlider(self.settings_box, from_=0.1, to=1.0, command=self.update_smoothing)
        self.smoothing.set(0.5)
        self.smoothing.pack(pady=5)
        self.smoothing_label = ctk.CTkLabel(self.settings_box, text="Smoothing: 0.50")
        self.smoothing_label.pack()

        self.confidence = ctk.CTkSlider(self.settings_box, from_=0.1, to=1.0, command=self.update_confidence)
        self.confidence.set(0.25)
        self.confidence.pack(pady=5)
        self.confidence_label = ctk.CTkLabel(self.settings_box, text="Confidence: 0.25")
        self.confidence_label.pack()

        self.fov = ctk.CTkSlider(self.settings_box, from_=20, to=200, command=self.update_fov)
        self.fov.set(60)
        self.fov.pack(pady=5)
        self.fov_label = ctk.CTkLabel(self.settings_box, text="FOV: 60px")
        self.fov_label.pack()

        # Theme Box
        self.theme_box = ctk.CTkFrame(self.right_section)
        self.theme_box.pack(fill="x", pady=10, padx=5)

        theme_label = ctk.CTkLabel(self.theme_box, text="APPEARANCE", font=("Roboto", 16, "bold"))
        theme_label.pack(pady=5)

        themes = ["dark", "light"]
        self.theme = ctk.CTkComboBox(self.theme_box, values=themes, command=self.change_theme)
        self.theme.set("dark")
        self.theme.pack(pady=5)

    def create_main_content(self):
        # Create preview area
        self.preview_frame = ctk.CTkFrame(self.left_section)
        self.preview_frame.pack(fill="both", expand=True, pady=(0,10))
        
        preview_label = ctk.CTkLabel(self.preview_frame, text="PREVIEW", font=("Roboto", 20, "bold"))
        preview_label.pack(pady=10)

        # About section
        self.about_frame = ctk.CTkFrame(self.left_section)
        self.about_frame.pack(fill="both", pady=10)

        about_text = """Long Range Aimbot Pro v2.0
        
Created by VirusterDev

Features:
• Advanced player detection with YOLOv5
• Highly customizable settings
• Smooth aim assist with adjustable parameters  
• Optimized for maximum performance
• Real-time preview and monitoring

Premium Features Available:
• Full aimbot capabilities
• Triggerbot functionality
• Enhanced visual features
• Resource optimization
• Priority support

Contact for premium version and custom solutions."""

        self.about = ctk.CTkTextbox(self.about_frame, wrap="word", height=200)
        self.about.pack(pady=10, padx=10, fill="both", expand=True)
        self.about.insert("1.0", about_text)
        self.about.configure(state="disabled")

    def toggle_aimbot(self):
        self.is_enabled = self.enabled.get()
        
    def update_rate_value(self, value):
        self.update_fps = int(value)
        self.update_rate_label.configure(text=f"Update Rate: {self.update_fps} FPS")
        
    def update_smoothing(self, value):
        self.smooth_factor = float(value)
        self.smoothing_label.configure(text=f"Smoothing: {self.smooth_factor:.2f}")
        
    def update_confidence(self, value):
        self.conf_threshold = float(value)
        self.confidence_label.configure(text=f"Confidence: {self.conf_threshold:.2f}")
        
    def update_fov(self, value):
        self.box_size = int(value)
        self.fov_label.configure(text=f"FOV: {self.box_size}px")
        
    def change_theme(self, theme):
        ctk.set_appearance_mode(theme)

menu = CheatMenu()
model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
model.classes = [0]
model.conf = menu.conf_threshold
model.iou = 0.45
model = model.cpu()
model.eval()

screen_width, screen_height = pyautogui.size()
last_detection_time = time.time()

while True:
    menu.window.update()
    
    if menu.is_enabled:
        current_time = time.time()
        if current_time - last_detection_time >= 1/menu.update_fps:
            capture_area = (
                screen_width//2 - menu.box_size//2,
                screen_height//2 - menu.box_size//2,
                screen_width//2 + menu.box_size//2,
                screen_height//2 + menu.box_size//2
            )
            
            frame = np.array(ImageGrab.grab(bbox=capture_area))
            
            with torch.no_grad():
                results = model(frame, size=64)
                detections = results.xyxy[0].cpu().numpy()
            
            if len(detections) > 0:
                center_x = menu.box_size // 2
                center_y = menu.box_size // 2
                closest_dist = float('inf')
                target_x = target_y = None
                
                for det in detections:
                    if det[5] == 0:
                        x1, y1, x2, y2 = det[:4]
                        det_center_x = (x1 + x2) / 2
                        det_center_y = (y1 + y2) / 2
                        
                        dist = ((det_center_x - center_x)**2 + (det_center_y - center_y)**2)**0.5
                        if dist < closest_dist:
                            closest_dist = dist
                            target_x = det_center_x
                            target_y = det_center_y
                
                if target_x is not None:
                    move_x = int((target_x - center_x) * menu.smooth_factor)
                    move_y = int((target_y - center_y) * menu.smooth_factor)
                    
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,
                                       move_x, move_y, 0, 0)
            
            last_detection_time = current_time
