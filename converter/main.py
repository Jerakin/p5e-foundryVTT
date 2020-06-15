from pathlib import Path
import shutil
import json
from converter import foundry

import converter.packages.pokemon as pokemon

PROJECT = Path(__file__).parent.parent

BUILD = PROJECT / "build"
BUILD_POKEMON = BUILD / "pokemon"

DIST = PROJECT / "dist"
DIST_MODULE = DIST / foundry.module_name
DIST_PACKS = DIST_MODULE / "packs"

DATA_SOURCE = Path(r"E:\projects\repositories\Pokedex5E\assets\datafiles")


def build_pokemon(input_file, output_file):
    with input_file.open() as fp:
        json_data = json.load(fp)
    poke = pokemon.Pokemon(input_file.stem, json_data)
    poke.save(output_file)


def build_move():
    pass


def build_item():
    pass


def build_ability():
    pass


def build():
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir()

    BUILD_POKEMON.mkdir()

    for pokemon_file in (DATA_SOURCE / "pokemon").iterdir():
        build_pokemon(pokemon_file, BUILD_POKEMON / pokemon_file.name)


def pack_folder(folder, output_file):
    with output_file.open("a") as fp:
        for p_file in folder.iterdir():
            with p_file.open() as f:
                fp.write(f.read() + "\n")


def package():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    DIST_MODULE.mkdir()
    DIST_PACKS.mkdir()

    for pack_name, pack_def in foundry.packs.items():
        if (BUILD / pack_name).exists():
            foundry.module_definition["packs"].append(pack_def)
            pack_folder(BUILD / pack_name, DIST_MODULE / pack_def["path"])

    with (DIST_MODULE / "module.json").open("w", encoding="utf-8") as fp:
        json.dump(foundry.module_definition, fp, indent=2, ensure_ascii=False)


def make():
    build()
    package()


if __name__ == "__main__":
    make()
