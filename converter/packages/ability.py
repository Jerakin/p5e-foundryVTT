import json
import converter.util as util
import hashlib

class Ability:
    def __init__(self, name, json_data):
        self.output_data = util.load_template("ability")
        self.output_data["name"] = name

        self.convert(json_data)
        if name in util.EXTRA_ABILITY_DATA:
            util.merge(self.output_data, util.EXTRA_ABILITY_DATA[name])

    def set_id(self):
        self.output_data["_id"] = hashlib.sha256(self.output_data["name"].encode('utf-8')).hexdigest()[:16]

    def convert(self, json_data):
        self.output_data["data"]["description"][
            "value"] = f'<p>{json_data["Description"]}</p>'
        self.set_id()

    def save(self, file_path):
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        with file_path.open("w+") as fp:
            json.dump(self.output_data, fp)
