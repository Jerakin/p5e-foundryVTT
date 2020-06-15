import json
from pathlib import Path

from converter.main import DATA_SOURCE, PROJECT


def load_datafile(name):
    p = Path(DATA_SOURCE / (name + ".json"))
    with p.open() as fp:
        json_data = json.load(fp)
    return json_data


def load_extra(name):
    p = Path(PROJECT / "converter" / "assets" / "extra" / (name + ".json"))
    with p.open() as fp:
        json_data = json.load(fp)
    return json_data


def load_template(name):
    p = Path(PROJECT / "converter" / "assets" / "templates" / (name + ".json"))
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