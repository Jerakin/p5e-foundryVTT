import sys
from pathlib import Path
from github_release import gh_release_create
import subprocess as cmd

def get_active_branch_name():
    head_dir = Path(".") / ".git" / "HEAD"
    with head_dir.open("r") as f: content = f.read().splitlines()
    for line in content:
        if line[0:4] == "ref:":
            return line.partition("refs/heads/")[2]


if not get_active_branch_name() == "release":
    print("aborting, not on 'release' branch")
    sys.exit(1)

module_version = (Path(__file__).parent.parent / "VERSION").read_text()
cmd.run("git add module.json")
cmd.run(f"git commit -m 'Update manifest to f{module_version}'")
cmd.run("git push")

gh_release_create("Jerakin/p5e-foundryVTT", f"v{module_version}", token=Path("~/Documents/signing/TOKEN_VTT").expanduser().read_text(), publish=True, name=f"v{module_version}", asset_pattern="dist/Pokemon5e.zip")
