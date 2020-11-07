import hashlib
import json
import math

import converter.packages.ability as ability
import converter.packages.move as move
import converter.packages.experience as experience
import converter.util as util
import converter.foundry as foundry
from converter import pokemon_types as p_types


class Move(move.Move):
    def __init__(self, json_data):
        self.output_data = json_data

        self.output_data["labels"] = {"featType": "", "activation": "", "target": "",
                                      "range": "", "duration": "", "recharge": "",
                                      "save": "", "damage": "", "damageTypes": ""}

    def convert(self, json_data=None):
        self.output_data["labels"]["featType"] = self.output_data["data"]["activation"]["type"].capitalize()
        self.output_data["labels"][
            "activation"] = f'{self.output_data["data"]["activation"]["cost"]} {self.output_data["labels"]["featType"]}'

        self.output_data["labels"][
            "target"] = f'{self.output_data["data"]["target"]["value"]} {self.output_data["data"]["target"]["type"].capitalize()}'

        self.output_data["labels"][
            "range"] = f'{self.output_data["data"]["range"]["value"]} {self.output_data["data"]["range"]["units"]}'

        self.output_data["labels"][
            "duration"] = f'{self.output_data["data"]["duration"]["value"]} {self.output_data["data"]["duration"]["units"].capitalize()}s'

        if self.output_data["data"]["recharge"]["value"]:
            self.output_data["labels"]["recharge"] = f'Recharge {self.output_data["data"]["recharge"]["value"]}'

        self.output_data["labels"][
            "save"] = f'DC {self.output_data["data"]["save"]["dc"]} {self.output_data["data"]["save"]["ability"].upper()}'
        self.output_data["labels"]["damage"] = self.output_data["data"]["damage"]["parts"][0][0]
        # self.output_data["labels"]["damageTypes"] = self.output_data["data"]["details"]["background"]


class Ability:
    def __init__(self, json_data):
        self.output_data = json_data

        self.output_data["labels"] = {"featType": "", "activation": "", "target": "",
                                      "range": "", "duration": "", "recharge": "",
                                      "save": "", "damage": "", "damageTypes": ""}
        self.convert()

    def convert(self):
        self.output_data["labels"]["featType"] = self.output_data["data"]["activation"]["type"].capitalize()
        self.output_data["labels"][
            "activation"] = f'{self.output_data["data"]["activation"]["cost"]} {self.output_data["labels"]["featType"]}'

        self.output_data["labels"][
            "target"] = f'{self.output_data["data"]["target"]["value"]} {self.output_data["data"]["target"]["type"].capitalize()}'

        self.output_data["labels"][
            "range"] = f'{self.output_data["data"]["range"]["value"]} {self.output_data["data"]["range"]["units"]}'

        self.output_data["labels"][
            "duration"] = f'{self.output_data["data"]["duration"]["value"]} {self.output_data["data"]["duration"]["units"].capitalize()}s'

        if self.output_data["data"]["recharge"]["value"]:
            self.output_data["labels"]["recharge"] = f'Recharge {self.output_data["data"]["recharge"]["value"]}'

        self.output_data["labels"][
            "save"] = f'DC {self.output_data["data"]["save"]["dc"]} {self.output_data["data"]["save"]["ability"].upper()}'
        # self.output_data["labels"]["damage"] = self.output_data["data"]["damage"]["parts"][0][0]
        # self.output_data["labels"]["damageTypes"] = self.output_data["data"]["details"]["background"]


class PokemonItem:
    def __init__(self, name, json_data):
        self.output_data = util.load_template("pokemon_item")
        self.output_data["name"] = name

        self.convert(json_data)

    def convert_image(self):
        self.output_data["img"] = util.EXTRA_POKEMON_ICON_DATA[self.output_data["name"]]["img"]

    def convert_move_info(self, json_data):
        lines = ["<h2>Moves</h2>",
                 "<p><strong>Starting Moves</strong>: {}</p>".format(", ".join(json_data["Moves"]["Starting Moves"]))]

        level_moves = {"2": "<p><strong>Level 2</strong>: {}</p>",
                       "6": "<p><strong>Level 6</strong>: {}</p>",
                       "10": "<p><strong>Level 10</strong>: {}</p>",
                       "14": "<p><strong>Level 14</strong>: {}</p>",
                       "18": "<p><strong>Level 18</strong>: {}</p>"}

        for level in [2, 6, 10, 14, 18]:
            if str(level) in json_data["Moves"]["Level"]:
                lines.append(level_moves[str(level)].format(", ".join(json_data["Moves"]["Level"][str(level)])))
        if "TM" in json_data["Moves"]:
            lines.extend(["<h2>TMs</h2>", "<p>{}</p>".format(", ".join([str(x) for x in json_data["Moves"]["TM"]]))])
        return lines

    def convert_level_data(self, json_data):
        lines = []
        if "evolve_text" in json_data:
            lines.append("<blockquote>{}</blockquote>".format(json_data["evolve_text"]))

        return lines

    def convert(self, json_data):
        self.convert_image()
        evolve_lines = self.convert_level_data(json_data)
        move_lines = self.convert_move_info(json_data)
        evolve_lines.extend(move_lines)
        self.output_data["data"]["description"]["value"] = "\n".join(evolve_lines).format()

        self.output_data["data"]["hitDice"] = f"d{json_data['Hit Dice']}"
        self.output_data["data"]["source"] = str(json_data["index"])
        self.output_data["data"]["subclass"] = str(json_data["index"])
        self.output_data["data"]["levels"] = json_data["MIN LVL FD"]


class Pokemon:
    def __init__(self, name, json_data):
        self.output_data = util.load_template("pokemon")
        if name in util.TRANSLATE_NAME:
            name = util.TRANSLATE_NAME[name]
        self.output_data["name"] = name
        self.output_data["token"]["name"] = name

        self.proficiency = util.LEVEL_DATA[str(json_data["MIN LVL FD"])]["prof"]

        self.convert(name, json_data)
        if name in util.MERGE_POKEMON_DATA:
            util.merge(self.output_data, util.MERGE_POKEMON_DATA[name])

    @staticmethod
    def _ability_modifier(value):
        return math.floor((value - 10) / 2)

    def set_id(self):
        self.output_data["_id"] = hashlib.sha256(self.output_data["name"].encode('utf-8')).hexdigest()[:16]

    def convert_token(self, json_data):
        self.output_data["token"]["img"] = util.EXTRA_POKEMON_IMAGE_DATA[self.output_data["name"]]["token"]

        size = self.output_data["data"]["traits"]["size"]
        self.output_data["token"]["width"] = foundry.token_size_map[size]["width"]
        self.output_data["token"]["height"] = foundry.token_size_map[size]["height"]
        self.output_data["token"]["scale"] = foundry.token_size_map[size]["scale"]

        if "Senses" not in json_data:
            return

        self.output_data["token"]["actorId"] = self.output_data["_id"]

        bright_sight = 0
        for sense_line in json_data["Senses"]:
            sense, amount = sense_line.split()
            sense = sense.lower()
            amount = int(amount.replace("ft", "").replace(".", ""))
            if sense == "darkvision":
                self.output_data["token"]["dimSight"] = amount
            else:
                bright_sight = max(bright_sight, amount)
        self.output_data["token"]["brightSight"] = bright_sight

    def add_starting_moves(self, json_data):
        for move_name in json_data["Moves"]["Starting Moves"]:
            if move_name in util.BUILD_MOVES.iterdir():  # Check if the move have been built and use that
                with (util.BUILD_MOVES / move_name).with_suffix(".json").open(encoding="utf-8") as fp:
                    json_move_data = json.load(fp)
                    new_move = Move(json_move_data)
            else:  # Move have not been built, build it and use that
                m, json_move_data = move.build_from_cache(move_name)
                new_move = Move(m.output_data)

            level = self.output_data["data"]["details"]["level"]

            _move = 0
            # Scale the move with the current pokemon modifier
            power = new_move.output_data["data"]["ability"]
            if power:
                if power == "any":
                    _move = max([self.output_data["data"]["abilities"][ab]["mod"]] for ab in foundry.abilities)
                elif power == "varies":
                    pass
                else:
                    _move = self.output_data["data"]["abilities"][power]["mod"]
            new_move.update_damage_save(json_move_data, level, self.proficiency, _move)
            new_move.convert()

            self.output_data["items"].append(new_move.output_data)

    def add_abilities(self, json_data):
        abilities = json_data["Abilities"]
        if "Hidden Ability" in json_data:
            abilities.append(json_data["Hidden Ability"])

        for ability_name in abilities:
            if ability_name in util.BUILD_ABILITIES.iterdir():  # Check if the ability have been built and use that
                with (util.BUILD_ABILITIES / ability_name).with_suffix(".json").open(encoding="utf-8") as fp:
                    json_ability_data = json.load(fp)
                    new_ability = Ability(json_ability_data)
            else:  # Abilities have not been built, build it and use that
                m, json_ability_data = ability.build_from_cache(ability_name)
                new_ability = Ability(m.output_data)

            self.output_data["items"].append(new_ability.output_data)

    def add_pokemon_item(self, name, json_data):
        item = PokemonItem(name, json_data)
        self.output_data["items"].append(item.output_data)

    def convert_dex_entry(self, json_data):
        pd = util.POKEDEX_DATA[str(json_data["index"])]
        entry = "<p>{description}</p>\n<p>Species: {genus}</p>\n<p>Height: {height}</p>\n<p>Weight {weight}</p>"
        self.output_data["data"]["details"]["biography"]["value"] = entry.format(genus=pd["genus"],
                                                                                 description=pd["flavor"],
                                                                                 height=f"{pd['height'] / 10} m",
                                                                                 weight=f"{pd['weight'] / 10} kg")
        self.output_data["data"]["details"]["biography"]["race"] = pd["genus"].replace("Pokémon", "")

    def convert_traits(self, json_data):
        """Resistance, Immunities, Vulnerabilities, Size"""
        model = p_types.Model(*json_data["Type"])
        self.output_data["data"]["traits"]["dr"]["custom"] = "; ".join([x.capitalize() for x in model.resistances])
        self.output_data["data"]["traits"]["di"]["custom"] = "; ".join([x.capitalize() for x in model.immunities])
        self.output_data["data"]["traits"]["dv"]["custom"] = "; ".join([x.capitalize() for x in model.vulnerabilities])
        self.output_data["data"]["traits"]["senses"] = ", ".join(json_data["Senses"]) if "Senses" in json_data else ""
        self.output_data["data"]["traits"]["size"] = foundry.abv_size[json_data["size"]]

    def convert_skills(self, json_data):
        """Athletics, Sleight of Hand, etc."""
        if "Skill" not in json_data:
            return
        skills = json_data["Skill"]
        for abv, name in foundry.skill_abv_to_name.items():
            _ability = self.output_data["data"]["skills"][abv]["ability"]
            mod = self.output_data["data"]["abilities"][_ability]["mod"]
            self.output_data["data"]["skills"][abv]["mod"] = mod

            add_prof = 0
            if name in skills:
                add_prof = self.proficiency
                self.output_data["data"]["skills"][abv]["value"] = 1

            self.output_data["data"]["skills"][abv]["prof"] = add_prof
            self.output_data["data"]["skills"][abv]["total"] = add_prof + mod
            self.output_data["data"]["skills"][abv]["passive"] = 10 + add_prof + mod

    def convert_details(self, json_data):
        self.output_data["data"]["details"]["background"] = "/".join(json_data["Type"])
        self.output_data["data"]["details"]["level"] = json_data["MIN LVL FD"]
        sr = json_data["SR"]
        self.output_data["data"]["details"]["alignment"] = foundry.sr_map[sr] if sr in foundry.sr_map else str(int(sr))
        self.output_data["data"]["details"]["race"] = util.POKEDEX_DATA[str(json_data["index"])]["genus"].replace("Pokémon",
                                                                                                             "")
        self.output_data["data"]["details"]["xp"]["value"] = experience.GRID[json_data["MIN LVL FD"]][
            json_data["SR"]]

        next_level = json_data["MIN LVL FD"] + 1
        if next_level == 21:
            next_level = 20
        self.output_data["data"]["details"]["xp"]["max"] = util.LEVEL_DATA[str(next_level)]["exp"]

    def convert_attributes(self, json_data):
        self.output_data["data"]["attributes"]["ac"]["value"] = json_data["AC"]
        self.output_data["data"]["attributes"]["hp"]["value"] = json_data["HP"]
        self.output_data["data"]["attributes"]["hp"]["max"] = json_data["HP"]

        self.output_data["data"]["attributes"]["speed"][
            "value"] = f'{json_data["WSp"]} ft' if "WSp" in json_data else "0 ft"

        self.output_data["data"]["attributes"]["init"]["mod"] = self.output_data["data"]["abilities"]["dex"]["mod"]

    def convert_movement_speed(self, json_data):
        translate = {"Ssp": "Swimming",
                     "Fsp": "Flying",
                     "Climbing Speed": "Climbing",
                     "Burrowing Speed": "Burrowing",
                     }
        all_speeds = []
        for speed, new in translate.items():
            if speed in json_data:
                all_speeds.append(f'{new} {json_data[speed]} ft')
        self.output_data["data"]["attributes"]["speed"]["special"] = ", ".join(all_speeds)

    def convert_abilities(self, json_data):
        """Strength, Dexterity, Constitution, etc."""
        saving_throws = json_data["saving_throws"] if "saving_throws" in json_data else []
        for name, value in json_data["attributes"].items():
            _ability = name.lower()
            current = self.output_data["data"]["abilities"][_ability]
            current["value"] = value
            current["mod"] = self._ability_modifier(value)
            current["save"] = current["mod"] + self.proficiency if name in saving_throws else 0
            current["prof"] = self.proficiency if name in saving_throws else 0
            current["proficient"] = 1 if name in saving_throws else 0

    def convert_stab(self, json_data):
        self.output_data["data"]["resources"]["primary"]["value"] = util.LEVEL_DATA[str(json_data["MIN LVL FD"])]["STAB"]

    def convert(self, name, json_data):
        self.set_id()

        self.convert_abilities(json_data)
        self.convert_attributes(json_data)
        self.convert_details(json_data)
        self.convert_skills(json_data)
        self.convert_traits(json_data)
        self.convert_dex_entry(json_data)
        self.convert_token(json_data)
        self.convert_movement_speed(json_data)

        self.add_pokemon_item(name, json_data)
        self.add_starting_moves(json_data)
        self.add_abilities(json_data)
        self.convert_stab(json_data)

    def save(self, file_path):
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        with file_path.open("w+", encoding="utf-8") as fp:
            json.dump(self.output_data, fp, ensure_ascii=False)
