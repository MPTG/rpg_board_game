import json


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