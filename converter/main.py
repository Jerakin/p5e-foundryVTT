from pathlib import Path
import shutil
import json
import math
from converter import foundry
import converter.pokemon_types as p_types
import hashlib

PROJECT = Path(__file__).parent.parent

data_files = Path(r"E:\projects\repositories\Pokedex5E\assets\datafiles")

pokemon_data_folder = data_files / "pokemon"


def load_datafile(name):
    p = Path(data_files / (name + ".json"))
    with p.open() as fp:
        json_data = json.load(fp)
    return json_data


def load_template(name):
    p = Path(PROJECT / "converter" / "templates" / (name + ".json"))
    with p.open() as fp:
        json_data = json.load(fp)
    return json_data


def load_extra(name):
    p = Path(PROJECT / "converter" / "extra" / (name + ".json"))
    with p.open() as fp:
        json_data = json.load(fp)
    return json_data


LEVEL_DATA = load_datafile("leveling")
EXTRA_MOVE_DATA = load_extra("moves")
EXTRA_POKEMON_DATA = load_extra("pokemon")


def merge(a, b, path=None):
    """merges b into a"""
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same value
            else:  # Overwrite value
                a[key] = b[key]
                # raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


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
        if not (PROJECT / "build" / "pokemon").exists():
            (PROJECT / "build" / "pokemon").mkdir()

        with file_path.open("w+") as fp:
            json.dump(self.output_data, fp)


def build_pokemon(input_file, output_file):
    with input_file.open() as fp:
        json_data = json.load(fp)
    pokemon = Pokemon(input_file.stem, json_data)
    pokemon.save(output_file)


def build_move():
    pass


def build_item():
    pass


def build_ability():
    pass


def build():
    if (PROJECT / "build").exists():
        shutil.rmtree(PROJECT / "build")
    (PROJECT / "build").mkdir()

    (PROJECT / "build" / "pokemon").mkdir()
    for pokemon_file in pokemon_data_folder.iterdir():
        build_pokemon(pokemon_file, PROJECT / "build" / "pokemon" / pokemon_file.name)


def pack_folder(folder, output_file):
    with output_file.open("a") as fp:
        for p_file in folder.iterdir():
            with p_file.open() as f:
                fp.write(f.read() + "\n")


def package():
    if (PROJECT / "dist").exists():
        shutil.rmtree(PROJECT / "dist")
    (PROJECT / "dist").mkdir()
    (PROJECT / "dist" / foundry.module_name).mkdir()
    (PROJECT / "dist" / foundry.module_name / "packs").mkdir()

    for pack_name, pack_def in foundry.packs.items():
        if (PROJECT / "build" / pack_name).exists():
            foundry.module_definition["packs"].append(pack_def)
            pack_folder(PROJECT / "build" / pack_name, PROJECT / "dist" / foundry.module_name / pack_def["path"])

    with (PROJECT / "dist" / foundry.module_name / "module.json").open("w", encoding="utf-8") as fp:
        json.dump(foundry.module_definition, fp, indent=2, ensure_ascii=False)


def make():
    build()
    package()


if __name__ == "__main__":
    make()
