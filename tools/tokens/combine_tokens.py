from PIL import Image
from pathlib import Path
import requests
import json
import shutil
from converter.util import CONVERTER, CACHE, ASSETS
from tools.utils import update_progress

root = CONVERTER
output = ASSETS / "images" / "token" / "tokens"
tokens = CACHE / "tokens"
token_source = ASSETS / "token" / "token_parts"
data_file = ASSETS / "data" / "pokemon_icons.json"
filter_data_path = Path(r"E:\projects\repositories\Pokedex5E\assets\datafiles\filter_data.json")

if not tokens.exists():
    tokens.mkdir(parents=True)

with data_file.open("r", encoding="utf-8") as fp:
    pokemon_data = json.load(fp)

with filter_data_path.open("r", encoding="utf-8") as fp:
    filter_data = json.load(fp)


def assemble(types, path, force=False):
    new_im = Image.open(token_source / "background.png")
    output_path = (output / path.name).with_suffix(".png")
    if output_path.exists() and not force:
        return

    if len(types) == 1:
        image1 = Image.open((token_source / types[0].lower()).with_suffix(".png"))
        new_im.paste(image1, mask=image1)
    else:
        mask = Image.open((token_source / "mask").with_suffix(".png"))
        image1 = Image.open((token_source / types[0].lower()).with_suffix(".png"))
        image2 = Image.open((token_source / types[1].lower()).with_suffix(".png"))
        ring = Image.composite(image1, image2, mask)
        new_im.paste(ring, mask=ring)
    token_image = Image.open(path)
    output_image = Image.alpha_composite(new_im, token_image)
    with open(output_path, "wb") as fp:
        output_image.save(fp)


def download_image(url, force=False):
    url_p = Path(url)
    path = tokens / url_p.name.replace("120px-", "")
    if path.exists() and not force:
        return path
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            return path
    else:
        print(f"Error {url_p.name}")


def main():
    total = len(pokemon_data)
    for index, (pokemon, data) in enumerate(pokemon_data.items()):
        update_progress(index/total)

        path = download_image(data["img"].replace("120px", "128px"))
        if path:
            assemble(filter_data[pokemon]["Type"], path)
            data["token"] = f"https://raw.githubusercontent.com/Jerakin/p5e-foundryVTT/master/assets/token/tokens/{path.name}"
        else:
            print(f'Could not download {data["img"].replace("120px", "128px")}')

    with data_file.open("w", encoding="utf-8") as fp:
        json.dump(pokemon_data, fp, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
