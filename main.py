import customtkinter as ctk

from Objects.GUI_objects import PlayerWindow, MapListWindow
from Objects.players import Player


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._set_appearance_mode("system")
        self.title("RPG board game")
        self.geometry("1080x900")

        self.label = ctk.CTkLabel(
            self,
            text="Dungeon Master's Menu",
            font=("Arial", 40, "italic"),
            )
        self.label.pack(pady=20)
        player = Player(self, 'files/dummy.json')
        player.pack(pady=20, padx=20, fill='both', expand=True)
        player.display_players_tabs()

        self.button_maps = ctk.CTkButton(
            self,
            text='Maps',
            command=self.open_map_list
        )
        self.button_maps.pack(side='bottom', pady=10, padx=20)

        self.players_window = None
        self.open_map_list_window = None

    def open_players_list(self):
        if self.players_window is None or not self.players_window.winfo_exists():
            self.players_window = PlayerWindow(self)
        else:
            self.players_window.focus()

    def open_map_list(self):
        if self.open_map_list_window is None or not self.open_map_list_window.winfo_exists():
            self.open_map_list_window = MapListWindow(self)
        else:
            self.open_map_list_window.focus()


if __name__ == "__main__":
    app = App()
    app.mainloop()
