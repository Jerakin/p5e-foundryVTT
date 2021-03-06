import json
import hashlib

import converter.util as util


class Ability:
    def __init__(self, name, json_data):
        self.output_data = util.load_template("ability")
        self.output_data["name"] = name

        self.convert(json_data)
        if name in util.MERGE_ABILITY_DATA:
            util.merge(self.output_data, util.MERGE_ABILITY_DATA[name])

    def set_id(self):
        self.output_data["_id"] = hashlib.sha256(self.output_data["name"].encode('utf-8')).hexdigest()[:16]

    def convert(self, json_data):
        self.output_data["data"]["description"][
            "value"] = f'<p>{json_data["Description"]}</p>'
        self.set_id()

    def save(self, file_path):
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        with file_path.open("w+", encoding="utf-8") as fp:
            json.dump(self.output_data, fp, ensure_ascii=False)


LOADED_ABILITY = {"json": None}


def build_from_cache(name):
    cached_move = (util.DATA / "abilities.json")
    if not cached_move.exists():
        raise FileNotFoundError(f"Can not find file: {cached_move}")
    if not LOADED_ABILITY["json"]:
        with cached_move.open() as fp:
            json_data = json.load(fp)
        LOADED_ABILITY["json"] = json_data
    data = LOADED_ABILITY["json"][name]
    m = Ability(name, data)
    m.save((util.BUILD_MOVES / name).with_suffix(".json"))
    return m, data