import json
from pathlib import Path
from datetime import datetime

from converter import main
import converter
import converter.foundry as foundry
import converter.util as util

# Build the project
main.make()


# Update the manifest
for pack_name, pack_def in foundry.packs.items():
    if (util.BUILD / pack_name).exists():
        foundry.module_definition["packs"].append(pack_def)

with (util.PROJECT / "module.json").open("w", encoding="utf-8") as fp:
    json.dump(foundry.module_definition, fp, indent=2, ensure_ascii=False)

tool_version = converter.__version__

# date of the data
data_date = (Path('.') / "p5e-data" / "VERSION").read_text()

# Converting the date to EU standard from US, which is then appended to the tool version
# This makes up the package version
date = datetime.strptime(data_date, "%m/%d/%Y").strftime("%y%m%d")
module_version = f"{tool_version}.{date}"

# Save the VERSION
with (Path(__file__).parent.parent / "VERSION").open('w') as fp:
    fp.write(module_version)
