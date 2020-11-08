import json
import time
import requests
import re
from pathlib import Path
import shutil
from PIL import Image

root = Path(__file__).parent.parent
output_json = root / "assets/data/pokemon_images.json"
input_folder = Path(__file__).parent.parent / "cache/pokemon"


class Bulbapedia:
    dirty_reg = re.compile("filehistory-selected[^\"]*.*?(cdn\.bulbagarden\.net/upload[^\"]*)")

    def image_exists(self, data, pokemon):
        if pokemon not in data:
            return False
        _img = data[pokemon]["image"]

        if _img:
            if (root / _img.replace("modules/Pokemon5e", "assets")).exists():
                return True
        return False

    def collect(self):
        if output_json.exists():
            with output_json.open("r") as fp:
                img_data = json.load(fp)

        new = {}
        for poke_json in input_folder.iterdir():
            with poke_json.open("r") as f:
                data = json.load(f)
                index = data["index"]
                pokemon = poke_json.stem
                raw_url = "https://bulbapedia.bulbagarden.net/wiki/File:{:03d}{}.png".format(index, pokemon)
                file_name = Path("./raw_images/{}{}.png".format(index, pokemon)).absolute()

            if not self.image_exists(img_data, pokemon):
                r = requests.get(raw_url)
                url = self.get_url_from_source(r.content)
                if url:
                    self.download_image(url, file_name)
                else:
                    print("No Match", pokemon)
                new[pokemon] = {"img": url}

        with output_json.open("w") as fp:
            json.dump(new, fp)

    def download_image(self, url, name):
        r = requests.get("http://" + url, stream=True)
        if r.status_code == 200:
            with open(name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            print("Error")

    def get_url_from_source(self, source):
        m = self.dirty_reg.search(str(source))
        if m:
            return m.group(1)
        return None

    def resize(self):
        size = 256, 256
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


class Pokedex5e:
    def main(self):
        new = {}
        for poke_json in input_folder.iterdir():
            with poke_json.open("r") as f:
                data = json.load(f)
                index = data["index"]
                pokemon = poke_json.stem

                raw_url = "https://raw.githubusercontent.com/Jerakin/Pokedex5E/master/assets/textures/pokemons/{}{}.png".format(index, pokemon)
                r = requests.get(raw_url)
                if r.status_code == 200:
                    pass
                else:
                    print("No Match", pokemon)
                new[pokemon] = {"img": raw_url}

        with output_json.open("w") as fp:
            json.dump(new, fp, indent=2)


def use_downloaded():
    with output_json.open("r") as fp:
        i_data = json.load(fp)

    for poke_json in input_folder.iterdir():
        with poke_json.open("r") as f:
            data = json.load(f)
            index = data["index"]
            pokemon = poke_json.stem
            if pokemon in i_data and i_data[pokemon]["image"] == "":
                i_data[pokemon]["image"] = f"modules/Pokemon5e/images/tokens/128px-Shuffle{index}.webp"

    with output_json.open("w") as f:
        json.dump(i_data, f, indent=4)


use_downloaded()
