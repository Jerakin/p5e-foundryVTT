import json
from pathlib import Path

PROJECT = Path(__file__).parent.parent.parent

pokemon_build_folder = PROJECT / "build" / "pokemon"

if pokemon_build_folder.exists():
    ids = []
    for file_path in pokemon_build_folder.iterdir():
        with file_path.open() as fp:
            data = json.load(fp)
            if data["_id"] in ids:
                print("Duplicated ID!")
            ids.append(data["_id"])
else:
    print("build directory not found")
