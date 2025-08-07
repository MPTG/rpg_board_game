import json
import os


class ReadJson():
    def __init__(self, file_path):
        self.file_path = file_path

    def read_json(self):
        # If file doesn't exist or is empty, return empty dict
        if not os.path.exists(self.file_path) or os.stat(self.file_path).st_size == 0:
            return {}

        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            # Corrupted file, return empty dict instead of crashing
            return {}


class WriteJson():
    def __init__(self, file_path):
        if not file_path.endswith('.json'):
            raise ValueError("File path must end with '.json'")
        if not file_path:
            raise ValueError("File path cannot be empty")
        
        self.file_path = file_path

    def append_json(self, data):
        """
        Appends or updates a single player's data in a JSON file.

        :param data: Dictionary of format {player_name: player_data}
        """
        all_data = {}

        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                try:
                    all_data = json.load(file)
                except json.JSONDecodeError:
                    print("Warning: JSON file is corrupted or empty. Overwriting.")

        all_data.update(data)

        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(all_data, file, indent=4, ensure_ascii=False)
    

    @staticmethod
    def save_data_to_json(file_path, data):
        """
        Saves the provided data to a JSON file.

        :param data: Dictionary to be saved.
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)