import json
import requests
from pathlib import Path

PROJECT = Path(__file__).parent.parent.parent

asset_folder = PROJECT / "assets"

with (asset_folder / "data" / "pokemon.json").open() as fp:
    data = json.load(fp, encoding="utf-8")

for pokemon, d in data.items():
    img_url = d["img"]
    r = requests.get(img_url)
    if r.status_code == 404:
        print(pokemon)
