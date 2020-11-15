import sys
import json
from pathlib import Path
import subprocess as cmd

import converter.foundry as foundry
import converter.util as util


def get_active_branch_name():
    head_dir = Path(".") / ".git" / "HEAD"
    with head_dir.open("r") as f: content = f.read().splitlines()
    for line in content:
        if line[0:4] == "ref:":
            return line.partition("refs/heads/")[2]


if not get_active_branch_name() == "release":
    print("aborting, not on 'release' branch")
    sys.exit(1)

# Update the manifest
with (util.PROJECT / "module.json").open("w", encoding="utf-8") as fp:
    json.dump(foundry.module_definition, fp, indent=2, ensure_ascii=False)

module_version = foundry.module_version

# Add the module json and a tag, push them both
cmd.run("git add VERSION")
cmd.run("git add module.json")
cmd.run(f'git commit -m "Update manifest to {module_version}"')
cmd.run(f'git tag -a v{module_version} -m "Release of {module_version}"')
cmd.run("git push origin release")
cmd.run(f'git push origin v{module_version}')

# Get token and create a release
token = Path("~/Documents/signing/TOKEN_VTT").expanduser().read_text()
cmd.run(f'githubrelease --github-token {token} release Jerakin/p5e-foundryVTT create v{module_version} --publish --name "v{module_version}" "dist/Pokemon5e.zip"')

