# src/components/buttons.py
import flet as ft

class PrimaryButton(ft.ElevatedButton):
    def __init__(self, text: str, on_click=None, padding=None, weight=None, **kwargs):
        
        super().__init__(**kwargs) 
        
        self.text = text
        self.on_click = on_click
        self.style = ft.ButtonStyle(
            color="#FFF6FE",
            bgcolor="#EF3961",
            padding=padding,
            text_style=ft.TextStyle(weight=weight)
        )