import tkinter as tk

class UIEffects:

    @staticmethod
    def apply_card_hover(frame, normal_bg="white", hover_bg="#F3F4F6"):
        """Hiệu ứng đổi màu nền đơn giản khi di chuột vào thẻ"""
        frame.bind("<Enter>", lambda e: frame.config(bg=hover_bg))
        frame.bind("<Leave>", lambda e: frame.config(bg=normal_bg))