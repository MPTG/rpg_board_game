from Objects.read_json import ReadJson
import customtkinter as ctk


class Player(ctk.CTkFrame):

    def __init__(self, master, data):
        super().__init__(master)

        self.data = ReadJson(data).read_json()
        self.tab = ctk.CTkTabview(
                self,
                width=800,
                height=600,
                corner_radius=10,
                fg_color="transparent",
                border_width=2,
                border_color="black"
                )
        self.tab.pack(pady=20, padx=20)

    def display_players_tabs(self):
        for i in self.data.keys():
            self.tab.add(i)

            frame = ctk.CTkFrame(self.tab.tab(i))
            frame.pack(pady=10, padx=20, fill='x')

            # Label on the left (name of the field)
            name_label = ctk.CTkLabel(
                frame,
                text=self.data[i]['name'],
                width=150,
                anchor='w',
                )

            name_label.pack(side='left', padx=(0, 10))

            # Entry in the middle (editable)
            entry = ctk.CTkEntry(frame, width=300)
            entry.pack(side='left', padx=(0, 10))

            # Label on the right (current value)
            value_label = ctk.CTkLabel(
                frame,
                text=self.data[i]['hp'], 
                width=150,
                anchor='w',
                )
            value_label.pack(side='left')