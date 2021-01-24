# Foundry VTT
This projects aim is to convert the [Pokemon5e](https://www.pokemon5e.com) Companion Apps data to a module for [Foundry VTT](https://foundryvtt.com/).

<p align="center">
  <img src="/.github/screenshot.png">
</p>

It addes the abilities, moves and the actual Pokemon from Pokemon5e into Foundry.

## Installation
See https://github.com/foundry-vtt-community/wiki/wiki/Modules#installing-modules. 

Open the Add-on Modules tab in the Configuration and Setup dialog. Click Install Module, paste `https://raw.githubusercontent.com/Jerakin/p5e-foundryVTT/release/module.json` in as the Manifest URL, then click Install.

As DM go to the Manage Modules options menu in the Game Settings for your World, then enable the Pokemon5e module.

### Manual Installation
If the above installation doesn't work you can try doing it manually.
1. Download the latest [release](https://github.com/Jerakin/p5e-foundryVTT/releases)
2. Unzip the file into a folder named `Pokemon5e` (*"Extract to Pokemon5e"*)
3. Place the folder `Pokemon5e` in `AppData/Local/FoundryVTT/Data/modules/` folder.

## Develop
### Requirements
Python 3.7 or higher as well as  
```
pip install requests
```

### Making a release
1. Change Branch to `release`
1. Update the `VERSION` file

**Get new data**  
This project have https://github.com/Jerakin/p5e-data-conversion added as submodule.  
1. Update, commit and push the submodule.
2. `python download.py path_to_token.json`.

**Build**  
1. Run `python build.py` and it will output the module content in `./dist*`

**Release**  
1. run `python release.py`
