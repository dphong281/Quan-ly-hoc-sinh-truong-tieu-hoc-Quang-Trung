import tkinter as tk

class CustomButton(tk.Button):
    def __init__(self, master, text, command, style_type="primary"):
        super().__init__(master, text=text, command=command)

        if style_type == "primary":
            self.config(bg="blue", fg="white")
        elif style_type == "success":
            self.config(bg="green", fg="white")