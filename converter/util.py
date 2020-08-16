import json
from pathlib import Path

import requests
import time
try:
    import gitdir as gitdir
    import foundry as foundry
except ImportError:
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

RAW_DATA_SOURCE = "https://raw.githubusercontent.com/Jerakin/Pokedex5E/p5e-vtt/assets/datafiles/"
DATA_SOURCE = "https://github.com/Jerakin/Pokedex5E/tree/p5e-vtt/assets/datafiles/"


def __load(path):
    with path.open(encoding="utf-8") as fp:
        json_data = json.load(fp)
    return json_data


def __get_index(index_entry, path):
    if path.exists():
        index_data = __load(path)
        if index_entry not in index_data:
            index_data[index_entry] = {}
    else:
        index_data = {index_entry: {}}
    return index_data


def __download(index_entry, path):
    index = CACHE / "index.json"
    index_data = __get_index(index_entry, index)

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    url = RAW_DATA_SOURCE + index_entry + ".json"
    r = requests.get(url)
    if r.status_code == 200:
        index_data[index_entry]["time"] = time.time()
        with index.open("w") as f:
            json.dump(index_data, f)

        data = json.loads(r.content.decode("utf-8"))
        with path.open("w", encoding="utf-8") as fp:
            json.dump(data, fp, ensure_ascii=False)
        return data
    else:
        print(url, r.status_code)


def _update_index(index_entry):
    index = CACHE / "index.json"
    index_data = __get_index(index_entry, index)
    if index_entry not in index_data:
        index_data[index_entry] = {}
    index_data[index_entry]["time"] = time.time()
    with index.open("w") as f:
        json.dump(index_data, f)


def _should_update(index_entry):
    index = CACHE / "index.json"
    index_data = __get_index(index_entry, index)
    current_time = time.time()
    if ("time" in index_data[index_entry] and current_time - index_data[index_entry]["time"] > 86400 * 7) or "time" not in index_data[index_entry]:  # Data is a week old
        return True


def __download_to_cache(index_entry, folder):
    if not (CACHE / folder).exists() or _should_update(index_entry):
        update = gitdir.download(DATA_SOURCE + folder, flatten=True, output_dir=CACHE / folder)
    else:
        return
    if update:
        _update_index(index_entry)


def download_pokemon():
    __download_to_cache("pokemon_data", "Pokemon")


def download_moves():
    __download_to_cache("moves_data", "moves")


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
ABILITY_DATA = load_datafile("abilities")

EXTRA_MOVE_DATA = load_extra("moves_extra")
EXTRA_POKEMON_DATA = load_extra("pokemon_extra")
MERGE_MOVE_DATA = load_extra("moves")
MERGE_POKEMON_DATA = load_extra("pokemon")
EXTRA_MOVE_ICON_DATA = load_extra("move_icons")
EXTRA_POKEMON_ICON_DATA = load_extra("pokemon_icons")
MERGE_ABILITY_DATA = load_extra("abilities")

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
