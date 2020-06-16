import hashlib
import json
import math
import re
from converter import pokemon_types as p_types
import converter.util as util


class Move:
    RANGE_REG = re.compile("([\d]+)")

    def __init__(self, name, json_data):
        self.output_data = util.load_template("move")
        self.output_data["name"] = name

        self.convert(json_data)
        if name in util.EXTRA_MOVE_DATA:
            util.merge(self.output_data, util.EXTRA_MOVE_DATA[name])

    def convert_range(self, json_data):
        _range = self.RANGE_REG.match(json_data["Duration"])
        if _range:
            _range = _range.group(1)
        else:
            _range = 0

        self.output_data["data"]["range"]["value"] = _range

    def convert_uses(self, json_data):
        self.output_data["data"]["uses"]["value"] = json_data["PP"]
        self.output_data["data"]["uses"]["max"] = json_data["PP"]

    def convert_activation(self, json_data):
        self.output_data["data"]["activation"]["type"] = json_data["Duration"].lower()

    def convert_ability(self, json_data):
        self.output_data["data"]["ability"] = ", ".join(json_data["Move Power"]) if "Move Power" in json_data else "None"

    def convert_damage(self, json_data):
        if "Damage" in json_data:
            amount = json_data["Damage"]["1"]["amount"]
            dice_max = json_data["Damage"]["1"]["dice_max"]
            self.output_data["data"]["damage"]["parts"] = ["{}d{} + @mod".format(amount, dice_max), ""]

    def convert_description(self, json_data):

        template = self.output_data["data"]["description"]["value"]
        icon = util.EXTRA_ICON_DATA[json_data["Type"].split("/")[0]]["img"]
        self.output_data["data"]["description"]["value"] = template.format(type_icon=icon, description=json_data["Description"], later_levels="")

    def convert(self, json_data):
        self.convert_description(json_data)
        self.convert_ability(json_data)
        self.convert_activation(json_data)
        self.convert_damage(json_data)
        self.convert_range(json_data)
        self.convert_uses(json_data)

    def save(self, file_path):
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        with file_path.open("w+") as fp:
            json.dump(self.output_data, fp)


# if __name__ == "__main__":
#     import shutil
#     from pathlib import Path
#     shutil.rmtree(util.BUILD_MOVES, ignore_errors=True)
#     for _name, _json_data in util.load_datafile("moves").items():
#         poke = Move(_name, _json_data)
#         poke.save((Path(r"E:\projects\repositories\p5e-foundryVTT\build") / _name).with_suffix(".json"))
