import requests
import json
import re
import shutil
from pathlib import Path
from converter.util import BUILD_POKEMON, PROJECT, CACHE
import time
from converter.tools.utils import update_progress
from PIL import Image

extra_pokemon = Path(PROJECT / "assets" / "data" / "pokemon_images").with_suffix(".json")

# index_orders = Path(RAW_DATA_SOURCE / "index_order").with_suffix(".json")
input_folder = CACHE / "pokemon"


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
                json_data[json_path.stem] = {}
            json_data[json_path.stem]["img"] = url
        else:
            print(pokemon)
        time.sleep(0.5)

    with extra_pokemon.open("w", encoding="utf-8") as fp:
        json.dump(json_data, fp, ensure_ascii=False, indent="  ")


def download_image(url, name):
    r = requests.get("http://" + url, stream=True)
    if r.status_code == 200:
        with open(name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        print("Error")


def add_tokens():
    dirty_reg = re.compile(r"filehistory-selected[^\"]*.*?(archives\.bulbagarden\.net/media/upload[^\"]*)")

    with extra_pokemon.open(encoding="utf-8") as fp:
        json_data = json.load(fp)

    def get_url_from_source(source):
        m = dirty_reg.search(str(source))
        if m:
            return m.group(1)

        return None

    # with index_orders.open(encoding="utf-8") as fp:
    #     index_json_data = json.load(fp)

    log = []
    for index, poke_json in enumerate(input_folder.iterdir()):
        pokemon = poke_json.stem
        with poke_json.open("r") as f:
            data = json.load(f)
        if pokemon in json_data and json_data[pokemon]["token"] == "":
            index = data["index"]
            raw_url = f"https://archives.bulbagarden.net/wiki/File:Shuffle{int(index):03}.png"
            r = requests.get(raw_url)
            url = get_url_from_source(r.content)
            if url:
                file_name = Path(f"./raw_images/Shuffle{int(index):03}.png").absolute()
                download_image(url, file_name)
                json_data[pokemon]["token"] = f"modules/Pokemon5e/images/token/Shuffle{int(index):03}.webp"
            else:
                log.append(f"No Match {pokemon} {int(index):03}")
            time.sleep(0.5)

    with extra_pokemon.open("w", encoding="utf-8") as fp:
        json.dump(json_data, fp, ensure_ascii=False, indent="  ")

    [print(x) for x in log]


def resize():
    size = 128, 128
    p = Path(__file__).parent / "raw_images"
    out = Path(__file__).parent / "resized"

    for infile in p.iterdir():
        outfile = out / infile.name
        if infile != outfile:
            try:
                img = Image.open(infile)
                img.thumbnail(size, Image.ANTIALIAS)
                img.save(outfile.with_suffix(".webp"), "WebP")
            except IOError:
                print("cannot create thumbnail for '%s'" % infile)


def crop():
    p = Path(__file__).parent / "raw_images"
    p = Path(r"E:\projects\repositories\p5e-foundryVTT\assets\images\tokens")

    for infile in p.iterdir():
        try:
            img = Image.open(infile)
            before = img.size
            img = img.crop(img.getbbox())
            if before != img.size:
                img.save(infile)
        except IOError:
            print("cannot create thumbnail for '%s'" % infile)


crop()
