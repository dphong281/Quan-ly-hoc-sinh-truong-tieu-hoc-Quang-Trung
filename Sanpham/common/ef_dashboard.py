import tkinter as tk

class UIEffects:

    @staticmethod
    def apply_card_hover(frame, normal_bg="white", hover_bg="#F3F4F6"):
        frame.bind("<Enter>", lambda e: frame.config(bg=hover_bg))
        frame.bind("<Leave>", lambda e: frame.config(bg=normal_bg))

    @staticmethod
    def apply_button_hover(button, normal_bg="#0d62b8", hover_bg="#0a4d91"):
        button.bind("<Enter>", lambda e: button.config(bg=hover_bg))
        button.bind("<Leave>", lambda e: button.config(bg=normal_bg))