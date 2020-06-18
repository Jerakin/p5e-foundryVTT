import hashlib
import json
import math

from converter import pokemon_types as p_types, foundry
from converter.util import load_template, LEVEL_DATA, EXTRA_POKEMON_DATA, merge, POKEDEX_DATA, EXTRA_POKEMON_ICON_DATA


class Move:
    def __init__(self, name, json_data):
        self.output_data = load_template("pokemon_move")
        self.output_data["name"] = name
        self.output_data["token"]["name"] = name

        self.convert(json_data)
        if name in EXTRA_POKEMON_DATA:
            merge(self.output_data, EXTRA_POKEMON_DATA[name])


class PokemonItem:
    def __init__(self, name, json_data):
        self.output_data = load_template("pokemon_item")
        self.output_data["name"] = name

        self.convert(json_data)
        if name in EXTRA_POKEMON_DATA:
            merge(self.output_data, EXTRA_POKEMON_DATA[name])

    def convert_image(self):
        img = "icons/svg/mystery-man.svg"
        if self.output_data["name"] in EXTRA_POKEMON_ICON_DATA:
            img = EXTRA_POKEMON_ICON_DATA[self.output_data["name"]]
        self.output_data["img"] = img

    def convert_move_info(self, json_data):
        lines = ["<h2>Moves</h2>",
                 "<p><strong>Starting Moves</strong>: {}</p>".format(", ".join(json_data["Moves"]["Starting Moves"]))]

        level_moves = {"6": "<p><strong>Level 6</strong>: {}</p>",
                       "10": "<p><strong>Level 10</strong>: {}</p>",
                       "14": "<p><strong>Level 14</strong>: {}</p>",
                       "18": "<p><strong>Level 18</strong>: {}</p>"}

        for level in [6, 10, 14, 18]:
            if str(level) in json_data["Moves"]["Level"]:
                lines.append(level_moves[str(level)].format(", ".join(json_data["Moves"]["Level"][str(level)])))
            lines.extend(["<h2>TMs</h2>", "<p>{}}</p>".format(", ".join(json_data["Moves"]["TM"]))])

        self.output_data["data"]["description"]["value"] = "\n".join(lines).format()

    def convert(self, json_data):
        self.convert_image()
        self.convert_move_info(json_data)
        self.output_data["data"]["hitDice"] = f"d{json_data['Hit Dice']}"
        self.output_data["data"]["source"] = str(json_data["index"])
        self.output_data["data"]["levels"] = json_data["MIN LVL FD"]

    @property
    def data(self):
        return self.output_data


class Pokemon:
    def __init__(self, name, json_data):
        self.output_data = load_template("pokemon")
        self.output_data["name"] = name
        self.output_data["token"]["name"] = name

        self.proficiency = LEVEL_DATA[str(json_data["MIN LVL FD"])]["prof"]

        self.convert(name, json_data)
        if name in EXTRA_POKEMON_DATA:
            merge(self.output_data, EXTRA_POKEMON_DATA[name])

    @staticmethod
    def _ability_modifier(value):
        return math.floor((value - 10) / 2)

    def set_id(self):
        self.output_data["_id"] = hashlib.sha256(self.output_data["name"].encode('utf-8')).hexdigest()[:16]
        self.output_data["token"]["actorId"] = self.output_data["_id"]

    def add_pokemon_item(self, name, json_data):
        item = PokemonItem(name, json_data)
        self.output_data["items"].append(item)

    def convert_dex_entry(self, json_data):
        pd = POKEDEX_DATA[str(json_data["index"])]
        entry = "<p>{description}</p>\n<p>Species: {genus}</p>\n<p>Height: {height} kg</p>\n<p>Weight {weight} m</p>"
        self.output_data["details"]["biography"]["value"] = entry.format(genus=pd["genus"], description=pd["flavor"],
                                                                         height="{} m".format(pd["height"] / 10),
                                                                         weight="{} kg".format(pd["weight"] / 10))
        self.output_data["details"]["biography"]["race"] = pd["genus"].replace("Pokémon", "")

    def convert_traits(self, json_data):
        """Resistance, Immunities, Vulnerabilities"""
        model = p_types.Model(*json_data["Type"])
        self.output_data["data"]["traits"]["dr"]["custom"] = ", ".join(model.resistances)
        self.output_data["data"]["traits"]["di"]["custom"] = ", ".join(model.immunities)
        self.output_data["data"]["traits"]["dv"]["custom"] = ", ".join(model.vulnerabilities)
        self.output_data["data"]["traits"]["senses"] = ", ".join(json_data["Senses"]) if "Senses" in json_data else ""

    def convert_skills(self, json_data):
        """Athletics, Sleight of Hand, etc."""
        if "Skill" not in json_data:
            return
        skills = json_data["Skill"]
        for abv, name in foundry.skill_abv_to_name.items():
            ability = self.output_data["data"]["skills"][abv]["ability"]
            mod = self.output_data["data"]["abilities"][ability]["mod"]
            self.output_data["data"]["skills"][abv]["mod"] = mod

            if name in skills:
                self.output_data["data"]["skills"][abv]["prof"] = self.proficiency

            self.output_data["data"]["skills"][abv]["total"] = self.proficiency + mod
            self.output_data["data"]["skills"][abv]["passive"] = 10 + self.proficiency + mod

    def convert_details(self, json_data):
        self.output_data["data"]["details"]["background"] = "/".join(json_data["Type"])
        self.output_data["data"]["details"]["level"] = json_data["MIN LVL FD"]
        self.output_data["data"]["details"]["alignment"] = json_data["SR"]

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
        """Strength, Dexterity, Constitution, etc."""
        saving_throws = json_data["saving_throws"] if "saving_throws" in json_data else []
        for name, value in json_data["attributes"].items():
            ability = name.lower()
            current = self.output_data["data"]["abilities"][ability]
            current["value"] = value
            current["mod"] = self._ability_modifier(value)
            current["save"] = current["mod"] + self.proficiency if name in saving_throws else 0
            current["prof"] = self.proficiency if name in saving_throws else 0

    def convert(self, name, json_data):
        self.convert_abilities(json_data)
        self.convert_attributes(json_data)
        self.convert_details(json_data)
        self.convert_skills(json_data)
        self.convert_traits(json_data)
        self.convert_dex_entry(json_data)
        self.add_pokemon_item(name, json_data)

        self.set_id()

    def save(self, file_path):
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        with file_path.open("w+") as fp:
            json.dump(self.output_data, fp)
