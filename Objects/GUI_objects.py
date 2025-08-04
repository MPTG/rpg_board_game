import customtkinter as ctk
from Objects.read_json import WriteJson


class OpenPlayersList(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("700x500")

        self.label = ctk.CTkLabel(self, text="Current Players")
        self.label.pack(pady=20, padx=20)


class MapListWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("700x500")

        self.label = ctk.CTkLabel(self, text="Manage Maps")
        self.label.pack(pady=20, padx=20)


class ShowMoreSkillsWindow(ctk.CTkToplevel):
    def __init__(self, player_name, player_data):
        super().__init__()
        self.geometry("700x500")
        self.title(f"More Skills - {player_name}")
        self.player_name = player_name
        self.player_data = player_data  # This includes 'skills' and 'statistics'
        self.json_writer = WriteJson('files/players.json')
        self.label = ctk.CTkLabel(self, text="More Skills", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        # Button to update skills
        self.update_button = ctk.CTkButton(self, text="Update Skills", command=self.update_skills)
        self.update_button.pack(pady=5)

        # Scrollable Frame for skill display
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Store references to labels for easy updating
        self.skill_labels = {}

        # Initial display
        self.display_skills()

    def display_skills(self):
        self.skill_labels.clear()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        col = 0
        row = 0
        for skill, value in self.player_data['skills'].items():
            label = ctk.CTkLabel(
                self.scrollable_frame,
                text=f"{skill.capitalize()}: {value}",
                anchor='w',
                font=("Arial", 18)
            )
            label.grid(row=row, column=col, padx=10, pady=5, sticky='w')
            self.skill_labels[skill] = label

            row += 1
            if row > 5:
                row = 0
                col += 1

    def update_skills(self):
        skills_to_statistics = {
            "acrobatics": "dexterity", "animal_handling": "wisdom",
            "arcana": "intelligence", "athletics": "strength",
            "deception": "charisma", "history": "intelligence",
            "insight": "wisdom", "intimidation": "charisma",
            "investigation": "intelligence", "medicine": "wisdom",
            "nature": "intelligence", "perception": "wisdom",
            "performance": "charisma", "persuasion": "charisma",
            "religion": "intelligence", "sleight_of_hand": "dexterity",
            "stealth": "dexterity", "survival": "wisdom"
        }

        for skill, related_stat in skills_to_statistics.items():
            stat_value = self.player_data["statistics"].get(related_stat, 10)
            modifier = (stat_value - 10) // 2
            self.player_data["skills"][skill] = modifier

            # Update label in UI
            if skill in self.skill_labels:
                self.skill_labels[skill].configure(text=f"{skill.capitalize()}: {modifier}")
                self.json_writer.append_json({
                    self.player_name: self.player_data
                    })


class AddPlayer(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("700x900")
        self.title("Add New Player")
        self.json_writer = WriteJson('files/players.json')
        self.label = ctk.CTkLabel(self, text="Add New Player")
        self.label.pack(pady=20, padx=20)
        self.information = {
            "name": "", "character_name": "", "character_level": "",
            "race": "", "class": "", "armor_class": 0, "hit_points": 0,
            "initiative": 0, "speed": 0, "proficiency_bonus": 2,
            "statistics": {
                "strength": 0, "dexterity": 0, "constitution": 0,
                "intelligence": 0, "wisdom": 0, "charisma": 0},
            "skills": {
                "acrobatics": 0, "animal_handling": 0, "arcana": 0,
                "athletics": 0, "deception": 0, "history": 0,
                "insight": 0, "intimidation": 0, "investigation": 0,
                "medicine": 0, "nature": 0, "perception": 0,
                "performance": 0, "persuasion": 0, "religion": 0,
                "sleight_of_hand": 0, "stealth": 0, "survival": 0
            }
        }

        # Container for form
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(pady=10, padx=20, fill='both', expand=True)

        self.entries = {}
        row = 0
        for key in self.information:
            if key in ("statistics", "skills"):
                self.manage_statistics()
                continue

            label = ctk.CTkLabel(
                self.form_frame,
                text=f"{key.replace('_', ' ').title()}:",
                anchor='w',
                font=("Arial", 14, "italic")
            )
            label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

            entry = ctk.CTkEntry(
                self.form_frame,
                width=200
            )
            entry.insert(0, str(self.information[key]))  # default value
            entry.grid(row=row, column=1, padx=10, pady=5)

            self.entries[key] = entry  # save entry
            row += 1

        # Add Button
        submit_button = ctk.CTkButton(
            self,
            text="Submit",
            command=self.save_information
        )
        submit_button.pack(pady=10)

    def save_information(self):
        for key, entry in self.entries.items():
            if key == 'statistics':
                continue
            value = entry.get()
            if self.information[key] != "" and isinstance(self.information[key], int):
                try:
                    self.information[key] = int(value)
                except ValueError:
                    print(f"Wrong number: {key}")
            else:
                self.information[key] = value

        # Handle statistics separately
        for stat_key, stat_entry in self.entries['statistics'].items():
            try:
                self.information['statistics'][stat_key] = int(stat_entry.get())
            except ValueError:
                print(f"Wrong number for statistic: {stat_key}")

        # Calculate skills based on statistics
        self.manage_skills()
        # Get player name from information
        player_name = self.information.get("name", "unknown")
        self.json_writer.append_json({player_name: self.information})
        self.destroy()

    def manage_statistics(self):
        row = 0
        self.entries['statistics'] = {}
        for key in self.information['statistics']:
            label = ctk.CTkLabel(
                self.form_frame,
                text=f"{key.replace('_', ' ').title()}:",
                anchor='w',
                font=("Arial", 14, "italic")
            )
            label.grid(row=row, column=2, sticky="w", padx=10, pady=5)

            entry = ctk.CTkEntry(
                self.form_frame,
                width=200
            )
            entry.insert(0, str(self.information['statistics'][key]))  # default value
            entry.grid(row=row, column=3, padx=10, pady=5)
            self.entries['statistics'][key] = entry  # save entry
            row += 1
    
    def manage_skills(self):
        skills_to_statistics = {
            "acrobatics": "dexterity", "animal_handling": "wisdom",
            "arcana": "intelligence", "athletics": "strength",
            "deception": "charisma", "history": "intelligence",
            "insight": "wisdom", "intimidation": "charisma",
            "investigation": "intelligence", "medicine": "wisdom",
            "nature": "intelligence", "perception": "wisdom",
            "performance": "charisma", "persuasion": "charisma",
            "religion": "intelligence", "sleight_of_hand": "dexterity",
            "stealth": "dexterity", "survival": "wisdom"
        }
        for skill, related_stat in skills_to_statistics.items():
            stat_value = self.information["statistics"].get(related_stat, 10)
            modifier = (stat_value - 10) // 2
            self.information["skills"][skill] = modifier

        # Add more functionality as needed


class ShowMenuTab(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        self.menu_tab = ctk.CTkTabview(
            self,
            width=200,
            height=800,
            corner_radius=10,
            fg_color="transparent",
            border_width=2,
            border_color="white"
            )
        self.menu_tab.pack(pady=10, padx=10)
        self.players_window = None
        self.open_map_list_window = None
        self.add_new_player_window = None

    def show_menu(self):
        self.menu_tab.add("Menu")
        self.menu_tab.tab("Menu").configure(fg_color="transparent")

        self.label = ctk.CTkLabel(
            self.menu_tab.tab("Menu"),
            text="Menu",
            font=("Arial", 20, "bold")
        )
        self.label.pack(pady=20, padx=20)
        self.button_maps = ctk.CTkButton(
            self.menu_tab.tab("Menu"),
            text='Maps',
            command=self.open_map_list
        )
        self.button_maps.pack(side='top', pady=10, padx=0)
        self.button_players = ctk.CTkButton(
            self.menu_tab.tab("Menu"),
            text='Players',
            command=self.open_players_list
        )
        self.button_players.pack(side='top', pady=10, padx=10)
        self.button_add_player = ctk.CTkButton(
            self.menu_tab.tab("Menu"),
            text='Add Player',
            command=self.add_new_player
        )
        self.button_add_player.pack(side='top', pady=10, padx=10)

    def open_players_list(self):
        if self.players_window is None or not self.players_window.winfo_exists():
            self.players_window = OpenPlayersList(self)
            self.players_window.focus()
        else:
            self.players_window.focus()

    def open_map_list(self):
        if self.open_map_list_window is None or not self.open_map_list_window.winfo_exists():
            self.open_map_list_window = MapListWindow(self)
            self.open_map_list_window.focus()
        else:
            self.open_map_list_window.focus()

    def add_new_player(self):
        if self.add_new_player_window is None or not self.add_new_player_window.winfo_exists():
            self.add_new_player_window = AddPlayer(self)
            self.add_new_player_window.focus()
        else:
            self.add_new_player_window.focus()
