import shutil
import json
import time

from converter import foundry

from tools.utils import update_progress
import converter.util as util
import converter.packages.pokemon as pokemon
import converter.packages.move as move
import converter.packages.ability as ability


def build_pokemon(name, json_data, output_file):
    poke = pokemon.Pokemon(name, json_data)
    poke.save(output_file)


def build_move(name, json_data, output_file):
    poke = move.Move(name, json_data)
    poke.save(output_file)


def build_ability(name, json_data, output_file):
    abi = ability.Ability(name, json_data)
    abi.save(output_file)


def build():
    if util.BUILD.exists():
        shutil.rmtree(util.BUILD)
    util.BUILD.mkdir()

    util.BUILD_POKEMON.mkdir()
    util.BUILD_MOVES.mkdir()
    util.BUILD_ABILITIES.mkdir()

    print("Building Pokemon")
    total = len(list((util.DATA_SOURCE / "pokemon").iterdir()))
    for index, pokemon_file in enumerate((util.DATA_SOURCE / "pokemon").iterdir(), 1):
        if pokemon_file.stem == "MissingNo":
            continue
        update_progress(index/total)
        with pokemon_file.open(encoding="utf-8") as fp:
            json_data = json.load(fp)
        build_pokemon(pokemon_file.stem, json_data, util.BUILD_POKEMON / pokemon_file.name)

    print("Building Moves")
    total = len(util.MOVE_DATA)
    for index, (name, json_data) in enumerate(util.MOVE_DATA.items(), 1):
        if name == "Error":
            continue
        update_progress(index / total)
        if name not in util.BUILD_MOVES.iterdir():
            build_move(name, json_data, (util.BUILD_MOVES / name).with_suffix(".json"))

    print("Building Abilities")
    total = len(util.ABILITY_DATA)
    for index, (name, json_data) in enumerate(util.ABILITY_DATA.items(), 1):
        update_progress(index / total)
        if name not in util.BUILD_ABILITIES.iterdir():
            build_ability(name, json_data, (util.BUILD_ABILITIES / name).with_suffix(".json"))


def pack_folder(folder, output_file):
    print(f"Packing {folder.stem}")
    with output_file.open("w", encoding="utf-8") as fp:
        total = len(list(folder.iterdir()))
        for index, p_file in enumerate(folder.iterdir(), 1):
            update_progress(index / total)
            with p_file.open(encoding="utf-8") as f:
                fp.write(f.read() + "\n")


def data():
    if util.DATA.exists():
        shutil.rmtree(util.DATA)
    util.DATA.mkdir()

    poke = []
    for p_file in util.BUILD_POKEMON.iterdir():
        with p_file.open(encoding="utf-8") as fp:
            poke.append(json.load(fp))

    with (util.DATA / "pokemon.json").open("w", encoding="utf-8") as fp:
        json.dump(poke, fp, indent=2, ensure_ascii=False)

    moves = []
    for p_file in util.BUILD_MOVES.iterdir():
        with p_file.open(encoding="utf-8") as fp:
            moves.append(json.load(fp))

    with (util.DATA / "moves.json").open("w", encoding="utf-8") as fp:
        json.dump(moves, fp, indent=2, ensure_ascii=False)

    abilities = []
    for p_file in util.BUILD_ABILITIES.iterdir():
        with p_file.open(encoding="utf-8") as fp:
            abilities.append(json.load(fp))

    with (util.DATA / "abilities.json").open("w", encoding="utf-8") as fp:
        json.dump(moves, fp, indent=2, ensure_ascii=False)

    shutil.copy(util.PROJECT / "foundryJS" / "import.js", util.DATA)


def package():
    if util.DIST.exists():
        shutil.rmtree(util.DIST)
    util.DIST.mkdir()
    util.DIST_MODULE.mkdir()
    util.DIST_PACKS.mkdir()

    for pack_name, pack_def in foundry.packs.items():
        if (util.BUILD / pack_name).exists():
            foundry.module_definition["packs"].append(pack_def)
            pack_folder(util.BUILD / pack_name, util.DIST_MODULE / pack_def["path"])

    with (util.DIST_MODULE / "module.json").open("w", encoding="utf-8") as fp:
        json.dump(foundry.module_definition, fp, indent=2, ensure_ascii=False)


def make():
    build()
    time.sleep(1)
    package()
    data()
    print("All done")


if __name__ == "__main__":
    make()
