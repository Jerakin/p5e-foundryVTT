import json
import time
import requests
import re
from pathlib import Path
import shutil
from PIL import Image

output_json = Path(__file__).parent.parent / "assets/data/pokemon.json"
input_folder = Path(__file__).parent.parent / "cache/pokemon"


class Bulbapedia:
    dirty_reg = re.compile("filehistory-selected[^\"]*.*?(cdn\.bulbagarden\.net/upload[^\"]*)")

    def collect(self):
        new = {}
        for poke_json in input_folder.iterdir():
            with poke_json.open("r") as f:
                data = json.load(f)
                index = data["index"]
                pokemon = poke_json.stem

                raw_url = "https://bulbapedia.bulbagarden.net/wiki/File:{:03d}{}.png".format(index, pokemon)
                file_name = Path("./raw_images/{}{}.png".format(index, pokemon)).absolute()

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
    new = {}
    with output_json.open("r") as fp:
        data = json.load(fp)

    for poke_json in input_folder.iterdir():
        with poke_json.open("r") as f:
            data = json.load(f)
            index = data["index"]
            pokemon = poke_json.stem
            new[pokemon] = {"img": f"modules/Pokemon5e/images/pokemon/{index}{pokemon}.webp"}

    with output_json.open("w") as f:
        data = json.dump(new, f, indent=4)

from pathlib import Path
import requests
import time
import shutil
import re
from bs4 import BeautifulSoup

import numpy as np

root = Path(__file__).parent
output = root / "images"
dirty_reg = re.compile('<a class="internal" href="(//archives.bulbagarden.net/media/upload.*)" title="BT{3}.png">BT{3}.png</a>')

if not output.exists():
    output.mkdir()


def crop(png_image_name):
    size = 128, 128
    im = Image.open(png_image_name)
    im.getbbox()
    im2 = im.crop(im.getbbox())
    im2.save(png_image_name.with_suffix(".webp"), "WebP")


def get_url_from_source(source):
    soup = BeautifulSoup(source, 'html.parser')
    for image in soup.find_all("img"):
        if image["height"] == "128" and image["width"] == "128":
            return image["src"][2:]
    return None


def download_image(url, name):
    r = requests.get("http://" + url, stream=True)
    print("Got Image ", name)
    if r.status_code == 200:
        with open(name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            print("Image copied")
    else:
        print("Error")


def download(index):
    # raw_url = "https://bulbapedia.bulbagarden.net/wiki/File:BT{:03d}.png".format(index,)
    raw_url = "https://bulbapedia.bulbagarden.net/wiki/File:BT{}.png".format(index,)
    file_name = Path(output / "128px-Shuffle{}.png".format(index)).absolute()

    r = requests.get(raw_url)
    url = get_url_from_source(r.content)
    if url:
        download_image(url, file_name)
        crop(file_name)
    else:
        print("No Match", index)


for img in Path(r"C:\Users\Jerakin\Downloads\t").iterdir():
    if img.suffix == ".png":
        # i = img.stem[-4:-1]
        crop(img)

# for i in range(720):
#     download(i+1)
    # time.sleep(0.5)

# if __name__ == '__main__':
# Bulbapedia().resize()

