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
        self.show_more_stats = None
        self.stat_entries = {}
        self.basic_info_entries = {}

    def display_players_tabs(self):
        self.frames = {}
        try:
            for player_name in self.data.keys():
                self.tab.add(player_name)

                frame_basic_info = ctk.CTkFrame(self.tab.tab(player_name))
                frame_basic_info.grid(
                    row=0,
                    column=0,
                    padx=(2, 10),
                    pady=10,
                    sticky='nsew'
                    )
                frame_stats = ctk.CTkFrame(self.tab.tab(player_name))
                frame_stats.grid(row=0, column=1, padx=(2, 10), pady=10)
                self.basic_info_entries[player_name] = {}
                row = 0
                for label, value in self.data[player_name].items():
                    if label == 'name':
                        continue

                    if label == 'character_name':
                        label_widget = ctk.CTkLabel(
                            frame_basic_info,
                            text=f'Character Name: {value}',
                            width=150,
                            anchor='w',
                            font=("Arial", 30, "bold"),
                        )
                        label_widget.grid(row=row, column=1, padx=(5, 0), pady=(10, 0))
                        row += 1
                        continue

                    if label in ('statistics', 'skills'):
                        self.show_and_update_statistics(player_name, frame_stats)
                        continue

                    # Editable entry for other fields (hit_points, armor_class, etc.)
                    ctk.CTkLabel(
                        frame_basic_info,
                        text=f"{label.capitalize()}:",
                        width=150,
                        anchor='w',
                        font=("Arial", 20, "italic"),
                    ).grid(row=row, column=0, padx=(0, 0), pady=(10, 0))

                    entry = ctk.CTkEntry(
                        frame_basic_info,
                        width=80,
                        font=("Arial", 20, "italic"),
                    )
                    entry.insert(0, str(value))
                    entry.grid(row=row, column=1, padx=(0, 0), pady=(10, 0))

                    self.basic_info_entries[player_name][label] = entry
                    row += 1

                # Add a save button for basic info
                save_info_btn = ctk.CTkButton(
                    frame_basic_info,
                    text="Save All",
                    command=lambda p=player_name: self.save_all(p)
                )
                save_info_btn.grid(row=row, column=0, columnspan=2, pady=(10, 0))

                self.frames[player_name] = frame_stats

                self.show_skills_button = ctk.CTkButton(
                    self.tab.tab(player_name),
                    text='Show More Skills',
                    command=lambda name=player_name: self.show_skills(name)
                )
                self.show_skills_button.grid(
                    row=row,
                    column=1,
                    padx=10,
                    pady=10,
                    sticky='ew'
                    )
                self.add_additional_informations(self.tab.tab(player_name))
        except KeyError:
            no_player_label = ctk.CTkLabel(
                self,
                text="No players found.",
                font=("Arial", 20, "italic"),
                justify='center',
            )
            no_player_label.pack(pady=20, padx=20)

    def show_skills(self, player_name):
        if self.show_more_stats is None or not self.show_more_stats.winfo_exists():
            self.show_more_stats = ShowMoreSkillsWindow(
                player_name,
                self.data[player_name],
                )
            self.show_more_stats.focus()
        else:
            self.show_more_stats.focus()
    
    def update_basic_info(self, player_name):
        for field, entry in self.basic_info_entries[player_name].items():
            val = entry.get()
            try:
                # Convert numeric strings to integers when possible
                if val.isdigit():
                    val = int(val)
            except ValueError:
                pass
            self.data[player_name][field] = val

        WriteJson.save_data_to_json(self.path_to_json, self.data)
        self.data = ReadJson(self.path_to_json).read_json()
        print(f"Updated basic info for {player_name}")

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
        self.additional_info.insert(
            "0.0", "Additional information about the player."
            )
        self.additional_info.grid(
            row=11,
            column=0,
            columnspan=3,
            padx=10,
            pady=10,
            sticky='nsew'
            )

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
    
    def save_all(self, player_name):
        # Update basic info
        for field, entry in self.basic_info_entries[player_name].items():
            val = entry.get()
            try:
                if val.isdigit():
                    val = int(val)
            except ValueError:
                pass
            self.data[player_name][field] = val

        # Update statistics
        for stat, entry in self.stat_entries[player_name].items():
            try:
                self.data[player_name]['statistics'][stat] = int(entry.get())
            except ValueError:
                print(f"Invalid value for {stat}: {entry.get()}")

        # Save changes to JSON
        WriteJson.save_data_to_json(self.path_to_json, self.data)
        self.data = ReadJson(self.path_to_json).read_json()

        # Refresh the player's tab
        self.refresh_player_tab(player_name)

        print(f"All data saved and refreshed for {player_name}")

    def refresh_player_tab(self, player_name):
        # Remove all widgets in this player's tab
        for widget in self.tab.tab(player_name).winfo_children():
            widget.destroy()

        # Rebuild the player tab UI from scratch
        frame_basic_info = ctk.CTkFrame(self.tab.tab(player_name))
        frame_basic_info.grid(row=0, column=0, padx=(2, 10), pady=10, sticky='nsew')

        frame_stats = ctk.CTkFrame(self.tab.tab(player_name))
        frame_stats.grid(row=0, column=1, padx=(2, 10), pady=10)

        self.basic_info_entries[player_name] = {}
        row = 0
        for label, value in self.data[player_name].items():
            if label == 'name':
                continue
            if label == 'character_name':
                label_widget = ctk.CTkLabel(
                    frame_basic_info,
                    text=f'Character Name: {value}',
                    width=150,
                    anchor='w',
                    font=("Arial", 30, "bold"),
                )
                label_widget.grid(row=row, column=1, padx=(5, 0), pady=(10, 0))
                row += 1
                continue
            if label in ('statistics', 'skills'):
                self.show_and_update_statistics(player_name, frame_stats)
                continue

            ctk.CTkLabel(
                frame_basic_info,
                text=f"{label.capitalize()}:",
                width=150,
                anchor='w',
                font=("Arial", 20, "italic"),
            ).grid(row=row, column=0, padx=(0, 0), pady=(10, 0))

            entry = ctk.CTkEntry(
                frame_basic_info,
                width=80,
                font=("Arial", 20, "italic"),
            )
            entry.insert(0, str(value))
            entry.grid(row=row, column=1, padx=(0, 0), pady=(10, 0))
            self.basic_info_entries[player_name][label] = entry
            row += 1

        save_info_btn = ctk.CTkButton(
            frame_basic_info,
            text="Save All",
            command=lambda p=player_name: self.save_all(p)
        )
        save_info_btn.grid(row=row, column=0, columnspan=2, pady=(10, 0))

        # Show skills button again
        self.show_skills_button = ctk.CTkButton(
            self.tab.tab(player_name),
            text='Show More Skills',
            command=lambda name=player_name: self.show_skills(name)
        )
        self.show_skills_button.grid(row=row, column=1, padx=10, pady=10, sticky='ew')

        self.add_additional_informations(self.tab.tab(player_name))