import json

from converter import main
import converter.foundry as foundry
import converter.util as util


# Update the manifest
for pack_name, pack_def in foundry.packs.items():
    if (util.BUILD / pack_name).exists():
        foundry.module_definition["packs"].append(pack_def)

with (util.PROJECT / "module.json").open("w", encoding="utf-8") as fp:
    json.dump(foundry.module_definition, fp, indent=2, ensure_ascii=False)

main.make()
