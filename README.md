# Foundry VTT
Pokmeon5e Module for [Foundry VTT](https://foundryvtt.com/).

## How to install
Download the newest [release](https://github.com/Jerakin/p5e-foundryVTT/releases),
unzip the file and place it in foundrys `./data/modules/` folder.

### Build
This projects aim is to convert the Pokemon5e Companion Apps data to a module for foundry.

If you for whatever reason want to convert it yourself you will need python 3.5 or higher.

You need a copy of the data files from the app and point towards them in the `./converter/main.py` file.

You can then simply run `python converter/main.py` and it will output the module content in `./dist*`
