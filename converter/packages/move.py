import hashlib
import json
import math

from converter import pokemon_types as p_types, foundry
from converter.main import PROJECT
from converter.util import load_template, LEVEL_DATA, EXTRA_MOVE_DATA, merge


class Move:
    def __init__(self, name, json_data):
        self.output_data = load_template("move")
        self.output_data["name"] = name

        self.convert(json_data)
        if name in EXTRA_MOVE_DATA:
            merge(self.output_data, EXTRA_MOVE_DATA[name])

    def convert(self, json_data):
        pass

    def save(self, file_path):
        file_path.parent.mkdir(parents=True)
        with file_path.open("w+") as fp:
            json.dump(self.output_data, fp)
