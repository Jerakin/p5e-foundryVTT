import json
from pathlib import Path
import converter.foundry as foundry

PROJECT = Path(__file__).parent.parent

BUILD = PROJECT / "build"
BUILD_POKEMON = BUILD / "pokemon"
BUILD_MOVES = BUILD / "moves"
BUILD_ABILITIES = BUILD / "abilities"

DIST = PROJECT / "dist"
DIST_MODULE = DIST / foundry.module_name
DIST_PACKS = DIST_MODULE / "packs"

DATA = PROJECT / "data"

DATA_SOURCE = Path(r"E:\projects\repositories\Pokedex5E\assets\datafiles")


def load_datafile(name):
    p = Path(DATA_SOURCE / name).with_suffix(".json")
    with p.open(encoding="utf-8") as fp:
        json_data = json.load(fp)
    return json_data


def load_extra(name):
    p = Path(PROJECT / "converter" / "assets" / "extra" / name).with_suffix(".json")
    with p.open(encoding="utf-8") as fp:
        json_data = json.load(fp)
    return json_data


def load_template(name):
    p = Path(PROJECT / "converter" / "assets" / "templates" / name).with_suffix(".json")
    with p.open(encoding="utf-8") as fp:
        json_data = json.load(fp)
    return json_data


LEVEL_DATA = load_datafile("leveling")
POKEDEX_DATA = load_datafile("pokedex_extra")
MOVE_DATA = load_datafile("moves")
ABILITY_DATA = load_datafile("abilities")

EXTRA_MOVE_DATA = load_extra("moves")
EXTRA_POKEMON_DATA = load_extra("pokemon")
EXTRA_MOVE_ICON_DATA = load_extra("move_icons")
EXTRA_POKEMON_ICON_DATA = load_extra("pokemon_icons")
EXTRA_ABILITY_DATA = load_extra("abilities")

TRANSLATE_NAME = {
  "Flabebe": "Flabébé",
  "Meowstic-f": "Meowstic ♀",
  "Meowstic-m": "Meowstic ♂",
  "Nidoran-m": "Nidoran ♂",
  "Nidoran-f": "Nidoran ♀"
}


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