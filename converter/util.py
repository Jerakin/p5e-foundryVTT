import json
from pathlib import Path

import requests
import time

import converter.gitdir as gitdir
import converter.foundry as foundry

PROJECT = Path(__file__).parent.parent
CONVERTER = PROJECT / "converter"

BUILD = PROJECT / "build"
BUILD_POKEMON = BUILD / "pokemon"
BUILD_MOVES = BUILD / "moves"
BUILD_ABILITIES = BUILD / "abilities"

DIST = PROJECT / "dist"
DIST_MODULE = DIST / foundry.module_name
DIST_PACKS = DIST_MODULE / "packs"

CACHE = PROJECT / "cache"

ASSETS = PROJECT / "assets"

RAW_DATA_SOURCE = "https://raw.githubusercontent.com/Jerakin/Pokedex5E/master/assets/datafiles/"
DATA_SOURCE = "https://github.com/Jerakin/Pokedex5E/tree/master/assets/datafiles/"


def __load(path):
    with path.open(encoding="utf-8") as fp:
        json_data = json.load(fp)
    return json_data


def __get_index(name, path):
    if path.exists():
        index_data = __load(path)
        if name not in index_data:
            index_data[name] = {}
    else:
        index_data = {name: {}}
    return index_data


def __download(name, path):
    index = CACHE / "index.json"
    index_data = __get_index(name, index)

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    url = RAW_DATA_SOURCE + name + ".json"
    r = requests.get(url)
    if r.status_code == 200:
        index_data[name]["time"] = time.time()
        with index.open("w") as f:
            json.dump(index_data, f)

        data = json.loads(r.content.decode("utf-8"))
        with path.open("w", encoding="utf-8") as fp:
            json.dump(data, fp, ensure_ascii=False)
        return data


def download_pokemon():
    name = "pokemon_data"
    index = CACHE / "index.json"
    index_data = __get_index(name, index)
    current_time = time.time()

    if "time" in index_data[name] and current_time - index_data[name]["time"] > 86400*7:  # Data is a week old
        total = gitdir.download(DATA_SOURCE + "pokemon", flatten=True, output_dir=CACHE / "pokemon")
    elif "time" not in index_data[name]:
        total = gitdir.download(DATA_SOURCE + "pokemon", flatten=True, output_dir=CACHE / "pokemon")
    else:
        return
    if total:
        if name not in index_data:
            index_data[name] = {}
        index_data[name]["time"] = time.time()
        with index.open("w") as f:
            json.dump(index_data, f)


def load_datafile(name):
    p = (CACHE / "data" / name).with_suffix(".json")
    index = CACHE / "index.json"
    if p.exists():
        if index.exists():
            index_data = __load(index)
            if name in index_data:
                current_time = time.time()
                if current_time - index_data[name]["time"] > 86400:  # Data is a day old
                    return __download(name, p)
        return __load(p)
    return __download(name, p)


def load_extra(name):
    p = Path(ASSETS / "data" / name).with_suffix(".json")
    return __load(p)


def load_template(name):
    p = Path(ASSETS / "templates" / name).with_suffix(".json")
    return __load(p)


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
