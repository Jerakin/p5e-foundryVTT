from pathlib import Path
import csv
import json

import converter.util as util

dex_data = Path("~").expanduser() / "Downloads" / "dexDATA.csv"
move_data = Path("~").expanduser() / "Downloads" / "moveDATA.csv"


def add_pokemon_size():
    with dex_data.open(encoding="utf-8") as fp:
        reader = csv.reader(fp)
        header = next(reader)
        pokemon_index = header.index("Pokemon")
        size_index = header.index("Size")
        for row in reader:
            pokemon = row[pokemon_index]
            size = row[size_index]
            if size and pokemon in util.EXTRA_POKEMON_DATA:
                util.EXTRA_POKEMON_DATA[pokemon]["data"] = {"traits": {"size": size.lower()}}
            else:
                print(pokemon)

        output = (util.ASSETS / "data" / "pokemon").with_suffix(".json")
        with output.open("w", encoding="utf-8") as f:
            json.dump(util.EXTRA_POKEMON_DATA, f, ensure_ascii=False, indent=2)


def add_move_higher_level():
    with move_data.open(encoding="utf-8") as fp:
        reader = csv.reader(fp)
        header = next(reader)
        move_index = header.index("Moves")
        data_index = header.index("Higher Level")
        new_data = {}
        for row in reader:
            move = row[move_index].strip()
            data = row[data_index]
            if data and f"{move}.json" in [x.name for x in util.BUILD_MOVES.iterdir()]:
                new_data[move] = {"hl": data}
            else:
                if data:
                    print(f"{move}.json")

        output = (util.ASSETS / "data" / "moves_extra").with_suffix(".json")
        with output.open("w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)