import hashlib
import json
import math
import re
from converter import pokemon_types as p_types
import converter.util as util


class Move:
    RANGE_REG = re.compile("([\d]+)")
    DURATION_REG = re.compile("([-d\d]+)\s([\w]+)")

    def __init__(self, name, json_data):
        self.output_data = util.load_template("move")
        self.output_data["name"] = name

        self.convert(json_data)
        if name in util.EXTRA_MOVE_DATA:
            util.merge(self.output_data, util.EXTRA_MOVE_DATA[name])

    def set_id(self):
        self.output_data["_id"] = hashlib.sha256(self.output_data["name"].encode('utf-8')).hexdigest()[:16]

    def convert_range(self, json_data):
        if json_data["Range"] == "Melee":
            _range = "0"
        else:
            _range = self.RANGE_REG.match(json_data["Range"])
            if _range:
                _range = _range.group(1)
            else:
                _range = 0

        self.output_data["data"]["range"]["value"] = _range

    def convert_uses(self, json_data):
        self.output_data["data"]["uses"]["value"] = json_data["PP"]
        self.output_data["data"]["uses"]["max"] = json_data["PP"]

    def convert_activation(self, json_data):
        move_time = json_data["Move Time"].lower()
        activation = ""
        if "bonus action" in move_time:
            activation = "bonus action"
        elif "action" in move_time:
            activation = "action"
        elif "reaction" in move_time:
            activation = "reaction"
        elif "bonus action" in move_time:
            activation = "bonus action"

        self.output_data["data"]["activation"]["type"] = activation

        if "Concentration" in json_data["Duration"]:
            self.output_data["data"]["activation"]["condition"] = "Concentration"

    def convert_duration(self, json_data):
        duration = json_data["Duration"].lower()
        if duration == "instantaneous":
            self.output_data["data"]["duration"]["units"] = "inst"
        else:

            dur = self.DURATION_REG.match(duration)
            if dur:
                dur.group(1)
                self.output_data["data"]["duration"]["value"] = dur.group(1)
                self.output_data["data"]["duration"]["units"] = dur.group(2)
            else:
                self.output_data["data"]["duration"]["units"] = "special"

    def convert_ability(self, json_data):
        self.output_data["data"]["ability"] = ", ".join(json_data["Move Power"]) if "Move Power" in json_data else "None"

    def convert_damage_save(self, json_data):
        if "Damage" in json_data:
            amount = json_data["Damage"]["1"]["amount"]
            dice_max = json_data["Damage"]["1"]["dice_max"]
            self.output_data["data"]["damage"]["parts"] = [["{}d{} + @mod".format(amount, dice_max), ""]]

        if "Save" in json_data:
            self.output_data["data"]["save"]["ability"] = json_data["Save"].lower()
            self.output_data["data"]["save"]["dc"] = 10
            self.output_data["data"]["save"]["scaling"] = json_data["Move Power"][0].lower() if "Move Power" in json_data else ""

    def convert_description(self, json_data):
        template = self.output_data["data"]["description"]["value"]
        icon = util.EXTRA_MOVE_ICON_DATA[json_data["Type"].split("/")[0]]["img"]
        self.output_data["data"]["description"]["value"] = template.format(type_icon=icon, description=json_data["Description"], later_levels="")

    def convert_icon(self, json_data):
        icon = util.EXTRA_MOVE_ICON_DATA[json_data["Type"].split("/")[0]]["icon"]
        self.output_data["img"] = icon

    def convert(self, json_data):
        self.convert_description(json_data)
        self.convert_ability(json_data)
        self.convert_activation(json_data)
        self.convert_damage_save(json_data)
        self.convert_range(json_data)
        self.convert_uses(json_data)
        self.convert_icon(json_data)
        self.convert_duration(json_data)

        self.set_id()

    def save(self, file_path):
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        with file_path.open("w+", encoding="utf-8") as fp:
            json.dump(self.output_data, fp, ensure_ascii=False)


# if __name__ == "__main__":
#     import shutil
#     from pathlib import Path
#     shutil.rmtree(util.BUILD_MOVES, ignore_errors=True)
#     for _name, _json_data in util.load_datafile("moves").items():
#         poke = Move(_name, _json_data)
#         poke.save((Path(r"E:\projects\repositories\p5e-foundryVTT\build") / _name).with_suffix(".json"))
