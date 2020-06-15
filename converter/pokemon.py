import hashlib
import json
import math

from converter import pokemon_types as p_types, foundry
from converter.main import PROJECT
from converter.util import load_template, LEVEL_DATA, EXTRA_POKEMON_DATA, merge


class Pokemon:
    def __init__(self, name, json_data):
        self.output_data = load_template("pokemon")
        self.output_data["name"] = name

        self.proficiency = LEVEL_DATA[str(json_data["MIN LVL FD"])]["prof"]

        self.convert(json_data)
        if name in EXTRA_POKEMON_DATA:
            merge(self.output_data, EXTRA_POKEMON_DATA[name])

    @staticmethod
    def _ability_modifier(value):
        return math.floor((value - 10) / 2)

    def set_id(self):
        self.output_data["_id"] = hashlib.sha256(self.output_data["name"].encode('utf-8')).hexdigest()[:16]

    def convert_traits(self, json_data):
        model = p_types.Model(*json_data["Type"])
        self.output_data["data"]["traits"]["dr"] = ", ".join(model.resistances)
        self.output_data["data"]["traits"]["di"] = ", ".join(model.immunities)
        self.output_data["data"]["traits"]["dv"] = ", ".join(model.vulnerabilities)
        self.output_data["data"]["traits"]["senses"] = ", ".join(json_data["Senses"]) if "Senses" in json_data else ""

    def convert_skills(self, json_data):
        if "Skill" not in json_data:
            return
        skills = json_data["Skill"]
        for abv, name in foundry.skill_abv_to_name.items():
            ability = self.output_data["data"]["skills"][abv]["ability"]
            mod = self.output_data["data"]["abilities"][ability]["mod"]
            self.output_data["data"]["skills"]["mod"] = mod

            if name in skills:
                self.output_data["data"]["skills"]["prof"] = self.proficiency

            self.output_data["data"]["skills"]["total"] = self.proficiency + mod
            self.output_data["data"]["skills"]["passive"] = 10 + self.proficiency + mod

    def convert_details(self, json_data):
        self.output_data["data"]["details"]["race"] = "/".join(json_data["Type"])
        self.output_data["data"]["details"]["level"] = json_data["MIN LVL FD"]

        next_level = json_data["MIN LVL FD"] + 1
        if next_level == 21:
            next_level = 20
        self.output_data["data"]["details"]["xp"]["max"] = LEVEL_DATA[str(next_level)]["exp"]

    def convert_attributes(self, json_data):
        self.output_data["data"]["attributes"]["ac"]["value"] = json_data["AC"]
        self.output_data["data"]["attributes"]["hp"]["value"] = json_data["HP"]
        self.output_data["data"]["attributes"]["hp"]["max"] = json_data["HP"]

        self.output_data["data"]["attributes"]["init"]["mod"] = self.output_data["data"]["abilities"]["dex"]["mod"]

    def convert_abilities(self, json_data):
        saving_throws = json_data["saving_throws"] if "saving_throws" in json_data else []
        for name, value in json_data["attributes"].items():
            ability = name.lower()
            current = self.output_data["data"]["abilities"][ability]
            current["value"] = value
            current["mod"] = self._ability_modifier(value)
            current["save"] = current["mod"] + self.proficiency if name in saving_throws else 0
            current["prof"] = self.proficiency if name in saving_throws else 0

    def convert(self, json_data):
        self.convert_abilities(json_data)
        self.convert_attributes(json_data)
        self.convert_details(json_data)
        self.convert_skills(json_data)
        self.convert_traits(json_data)

        self.set_id()

    def save(self, file_path):
        file_path.parent.mkdir(parents=True)
        with file_path.open("w+") as fp:
            json.dump(self.output_data, fp)