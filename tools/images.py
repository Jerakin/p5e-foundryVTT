import requests
import json
import re
from pathlib import Path
from converter.util import BUILD_POKEMON, PROJECT, DATA_SOURCE
import time
from tools.utils import update_progress

extra_pokemon = Path(PROJECT / "converter" / "assets" / "extra" / "pokemon").with_suffix(".json")
extra_pokemon_icons = Path(PROJECT / "converter" / "assets" / "extra" / "pokemon_icons").with_suffix(".json")

index_orders = Path(DATA_SOURCE / "index_order").with_suffix(".json")


def add_sprites():
    with extra_pokemon.open(encoding="utf-8") as fp:
        json_data = json.load(fp)

    for json_path in BUILD_POKEMON.iterdir():
        pokemon = json_path.stem
        pokemon = pokemon.lower().replace('- ', '').replace(' ', '-')
        pokemon = pokemon.replace('.', '').replace('Forme', '').replace('\'', '').strip()

        url = f"https://img.pokemondb.net/artwork/{pokemon}.jpg"
        r = requests.get(url)
        if r.status_code == 200:
            if pokemon not in json_data:
                json_data[pokemon] = {}
            json_data[pokemon]["img"] = url
        else:
            print(pokemon)
        time.sleep(0.5)

    with extra_pokemon.open("w", encoding="utf-8") as fp:
        json.dump(json_data, fp, ensure_ascii=False)


def add_tokens():
    dirty_reg = re.compile(r"filehistory-selected[^\"]*.*?(archives\.bulbagarden\.net/media/upload[^\"]*)")

    def get_url_from_source(source):
        m = dirty_reg.search(str(source))
        if m:
            return m.group(1)

        return None

    with index_orders.open(encoding="utf-8") as fp:
        index_json_data = json.load(fp)

    with extra_pokemon_icons.open(encoding="utf-8") as fp:
        json_data = json.load(fp)

    log = []
    amount = len(index_json_data)
    for index, pokemon_list in index_json_data.items():
        update_progress(int(index)/amount)

        raw_url = f"https://archives.bulbagarden.net/wiki/File:Shuffle{int(index):03}.png"
        r = requests.get(raw_url)
        url = get_url_from_source(r.content)
        if url:
            for pokemon in pokemon_list:
                if pokemon not in json_data:
                    json_data[pokemon] = {}
                json_data[pokemon]["img"] = url
        else:
            log.append(f"No Match {int(index):03}")
        time.sleep(0.5)

    with extra_pokemon_icons.open("w", encoding="utf-8") as fp:
        json.dump(json_data, fp, ensure_ascii=False)

    [print(x) for x in log]


add_tokens()
