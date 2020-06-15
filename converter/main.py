from pathlib import Path
import shutil
import json
from converter import foundry

from converter.pokemon import Pokemon

PROJECT = Path(__file__).parent.parent

data_files = Path(r"E:\projects\repositories\Pokedex5E\assets\datafiles")


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

    for pokemon_file in (data_files / "pokemon").iterdir():
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
