import customtkinter as ctk

import Objects.GUI_objects as gui_objects
from Objects.players import Player


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._set_appearance_mode("system")
        self.title("RPG board game")
        self.geometry("1400x720")

        self.label = ctk.CTkLabel(
            self,
            text="Dungeon Master's Menu",
            font=("Arial", 40, "italic"),
            )
        self.label.pack(pady=20, padx=20)
        menu = gui_objects.ShowMenuTab(self)
        menu.pack(side='left', pady=20, padx=20, fill='both')
        menu.show_menu()
        player = Player(self, 'files/players.json')
        player.pack(pady=20, padx=20, fill='both')
        player.display_players_tabs()


if __name__ == "__main__":
    app = App()
    app.mainloop()
