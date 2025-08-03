import json
import os


class ReadJson():
    def __init__(self, file_path):
        self.file_path = file_path

    def read_json(self):
        """
        Reads a JSON file and returns the data as a Python dictionary.

        :param file_path: Path to the JSON file.
        :return: Dictionary containing the JSON data.
        :raises FileNotFoundError: If the file does not exist.
        :raises json.JSONDecodeError: If the file is not a valid JSON.
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data


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