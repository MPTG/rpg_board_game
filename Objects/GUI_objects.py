import customtkinter as ctk


class PlayerWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("700x500")

        self.label = ctk.CTkLabel(self, text="Manage Players")
        self.label.pack(pady=20, padx=20)

  
class MapListWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("700x500")

        self.label = ctk.CTkLabel(self, text="Manage Maps")
        self.label.pack(pady=20, padx=20)
