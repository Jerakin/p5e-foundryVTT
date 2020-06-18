import requests
import json
from pathlib import Path
from converter.util import BUILD_POKEMON, PROJECT
import time


def add_sprites():
    p = Path(PROJECT / "converter" / "assets" / "extra" / "pokemon").with_suffix(".json")
    with p.open(encoding="utf-8") as fp:
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

    with p.open("w", encoding="utf-8") as fp:
        json.dump(json_data, fp, ensure_ascii=False)


add_sprites()
