import shutil
import json
from converter import foundry

import converter.util as util
import converter.packages.pokemon as pokemon
import converter.packages.move as move


def build_pokemon(name, json_data, output_file):
    poke = pokemon.Pokemon(name, json_data)
    poke.save(output_file)


def build_move(name, json_data, output_file):
    poke = move.Move(name, json_data)
    poke.save(output_file)


def build_item():
    pass


def build_ability():
    pass


def build():
    if util.BUILD.exists():
        shutil.rmtree(util.BUILD)
    util.BUILD.mkdir()

    util.BUILD_POKEMON.mkdir()
    util.BUILD_MOVES.mkdir()

    for pokemon_file in (util.DATA_SOURCE / "pokemon").iterdir():
        with pokemon_file.open() as fp:
            json_data = json.load(fp)
        build_pokemon(pokemon_file.stem, json_data, util.BUILD_POKEMON / pokemon_file.name)

    for name, json_data in util.MOVE_DATA.items():
        if name not in util.BUILD_MOVES.iterdir():
            build_move(name, json_data, (util.BUILD_MOVES / name).with_suffix(".json"))


def pack_folder(folder, output_file):
    with output_file.open("a") as fp:
        for p_file in folder.iterdir():
            with p_file.open() as f:
                fp.write(f.read() + "\n")


def data():
    if util.DATA.exists():
        shutil.rmtree(util.DATA)
    util.DATA.mkdir()

    poke = []
    for p_file in util.BUILD_POKEMON.iterdir():
        with p_file.open() as fp:
            poke.append(json.load(fp))

    with (util.DATA / "pokemon.json").open("w") as fp:
        json.dump(poke, fp)

    moves = []
    for p_file in util.BUILD_MOVES.iterdir():
        with p_file.open() as fp:
            moves.append(json.load(fp))

    with (util.DATA / "moves.json").open("w") as fp:
        json.dump(moves, fp)

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
    package()
    data()


if __name__ == "__main__":
    make()
