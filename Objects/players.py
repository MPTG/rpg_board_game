from Objects.read_json import ReadJson
from Objects.GUI_objects import ShowMoreSkillsWindow
import customtkinter as ctk


class Player(ctk.CTkFrame):

    def __init__(self, master, data):
        super().__init__(master)

        self.data = ReadJson(data).read_json()
        self.tab = ctk.CTkTabview(
                self,
                width=600,
                height=400,
                corner_radius=10,
                fg_color="transparent",
                border_width=2,
                border_color="white"
                )
        self.tab.pack(pady=10, padx=10)
        self.list_of_stats = [
            'HP',
            'Strength',
            'Dexterity',
            'Constitution',
            'Intelligence',
            'Wisdom',
            'Charisma'
            ]
        self.frames = []
        self.show_more_stats = None

    def display_players_tabs(self):
        self.frames = {}

        for player_name in self.data.keys():
            self.tab.add(player_name)

            frame_top = ctk.CTkFrame(self.tab.tab(player_name))
            frame_top.pack(pady=0, padx=0, fill='x')

            name_label = ctk.CTkLabel(
                frame_top,
                text=f'Character name: {self.data[player_name]['name']}',
                width=150,
                anchor='w',
                font=("Arial", 25, "italic"),
            )
            name_label.pack(side='top', padx=(0, 20), pady=(10, 0))

            self.frames[player_name] = []

            for stat_index in range(len(self.list_of_stats)):
                frame = ctk.CTkFrame(self.tab.tab(player_name))
                frame.pack(pady=5, padx=0, fill='x')
                self.frames[player_name].append(frame)
                self.stats_line_label(player_name, stat_index, frame)

            self.show_more_stats_button = ctk.CTkButton(
                self.tab.tab(player_name),
                text='Show More Skills',
                command=self.show_stats
            )
            self.show_more_stats_button.pack(
                side='bottom',
                pady=0,
                padx=0,
                )

    def stats_line_label(self, player_name, stat_index, frame):
        stat = self.list_of_stats[stat_index]

        if stat in self.data[player_name]:
            stat_label = ctk.CTkLabel(
                frame,
                text=f'Current {stat}',
                width=150,
                anchor='w',
                font=("Arial", 20, "italic"),
            )
            stat_label.pack(side='left', padx=(0, 10))

            stat_amount = ctk.CTkLabel(
                frame,
                text=str(self.data[player_name][stat]),
                width=50,
                anchor='w',
                font=("Arial", 20, "bold"),
            )
            stat_amount.pack(side='left', padx=(0, 10))

            new_stat_value = ctk.CTkLabel(
                frame,
                text=f'New {stat} Value',
                width=150,
                anchor='w',
                font=("Arial", 20, "italic"),
            )
            new_stat_value.pack(side='left', padx=(0, 10))

            entry = ctk.CTkEntry(frame, width=50)
            entry.pack(side='left', padx=(0, 10))

    def show_stats(self):
        if self.show_more_stats is None or not self.show_more_stats.winfo_exists():
            self.show_more_stats = ShowMoreSkillsWindow(self)
            self.show_more_stats.focus()
        else:
            self.show_more_stats.focus()
