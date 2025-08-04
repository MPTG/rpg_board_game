from Objects.read_json import ReadJson, WriteJson
from Objects.GUI_objects import ShowMoreSkillsWindow
import customtkinter as ctk


class Player(ctk.CTkFrame):

    def __init__(self, master, path_to_json):
        super().__init__(master)

        self.path_to_json = path_to_json
        self.data = ReadJson(self.path_to_json).read_json()
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
        self.frames = []
        self.show_more_stats = None
        self.stat_entries = {}

    def display_players_tabs(self):
        self.frames = {}

        for player_name in self.data.keys():
            self.tab.add(player_name)

            frame_basic_info = ctk.CTkFrame(self.tab.tab(player_name))
            frame_basic_info.grid(row=0, column=0, padx=(2, 10), pady=10, sticky='nsew')
            frame_stats = ctk.CTkFrame(self.tab.tab(player_name))
            frame_stats.grid(row=0, column=1, padx=(2, 10), pady=10)
            row = 0
            for label in self.data[player_name].keys():
                if label == 'name':
                    continue
                if label == 'character_name':
                    label = ctk.CTkLabel(
                        frame_basic_info,
                        text=(
                            f'Character Name: {self.data[player_name][label]}'
                            ),
                        width=150,
                        anchor='w',
                        font=("Arial", 30, "bold"),
                    )
                    label.grid(row=row, column=1, padx=(5, 0), pady=(10, 0))
                    row += 1
                    continue
                if label == 'statistics' or label == 'skills':
                    self.show_and_update_statistics(player_name, frame_stats)
                    continue
                label = ctk.CTkLabel(
                    frame_basic_info,
                    text=f'{label.capitalize()}: {self.data[player_name][label]}',
                    width=150,
                    anchor='w',
                    font=("Arial", 20, "italic"),
                )
                label.grid(row=row, column=0, padx=(0, 0), pady=(10, 0))
                row += 1

            self.frames[player_name] = frame_stats
            
            self.show_skills_button = ctk.CTkButton(
                self.tab.tab(player_name),
                text='Show More Skills',
                command=lambda name=player_name: self.show_skills(name)
            )
            self.show_skills_button.grid(row=row, column=1, padx=10, pady=10, sticky='ew')
            self.add_additional_informations(self.tab.tab(player_name))

    def show_skills(self, player_name):
        if self.show_more_stats is None or not self.show_more_stats.winfo_exists():
            self.show_more_stats = ShowMoreSkillsWindow(
                player_name,
                self.data[player_name]['skills']
                )
            self.show_more_stats.focus()
        else:
            self.show_more_stats.focus()

    def add_additional_informations(self, tab):
        self.additional_info = ctk.CTkTextbox(
            tab,
            width=500,
            height=100,
            corner_radius=10,
            fg_color="transparent",
            border_width=2,
            border_color="black"
        )
        self.additional_info.insert("0.0", "Additional information about the player.")
        self.additional_info.grid(row=11, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

    def show_and_update_statistics(self, player_name, frame):
        self.stat_entries[player_name] = {}
        row = 0
        for stat, value in self.data[player_name]['statistics'].items():
            label = ctk.CTkLabel(
                frame,
                text=f"{stat.capitalize()}: {value}",
                width=150,
                anchor='w',
                font=("Arial", 20, "italic"),
            )
            label.grid(row=row, column=1, padx=(0, 0), pady=(10, 0))
            entry_new_value = ctk.CTkEntry(
                frame,
                width=40,
                font=("Arial", 20, "italic"),
            )
            entry_new_value.insert(0, int(value))
            entry_new_value.grid(row=row, column=2, padx=(0, 0), pady=(10, 0))

            # Save entry for later use
            self.stat_entries[player_name][stat] = entry_new_value

            confirm_button = ctk.CTkButton(
                frame,
                text="Ok",
                command=lambda p=player_name: self.update_statistic(p),

                width=5,
            )

            confirm_button.grid(row=row, column=3, padx=(0, 0), pady=(10, 0))
            row += 1

    def update_statistic(self, player_name):
        for stat, entry in self.stat_entries[player_name].items():
            try:
                new_value = int(entry.get())
                self.data[player_name]['statistics'][stat] = new_value
            except ValueError:
                print(f"Invalid value for {stat}: {entry.get()}")

        WriteJson.save_data_to_json(self.path_to_json, self.data)  # ← Save to JSON file
        self.data = ReadJson(self.path_to_json).read_json()
        # Refresh the display
        self.frames[player_name].destroy()
        new_frame = ctk.CTkFrame(self.tab.tab(player_name))
        new_frame.grid(row=0, column=1, padx=(5, 10), pady=10)
        self.frames[player_name] = new_frame
        self.show_and_update_statistics(player_name, new_frame)
    
    def show_more_skills(self, player_name, frame):
        self.stat_entries[player_name] = {}
        row = 0
        for stat, value in self.data[player_name]['skills'].items():
            label = ctk.CTkLabel(
                frame,
                text=f"{stat.capitalize()}: {value}",
                width=150,
                anchor='w',
                font=("Arial", 20, "italic"),
            )
            label.grid(row=row, column=1, padx=(0, 0), pady=(10, 0))
