# Foundry VTT
This projects aim is to convert the [Pokemon5e](https://www.pokemon5e.com) Companion Apps data to a module for [Foundry VTT](https://foundryvtt.com/).

## Installation
1. Download the latest [release](https://github.com/Jerakin/p5e-foundryVTT/releases)
2. Unzip the file into a folder named `Pokemon5e` (*"Extract to Pokemon5e"*)
3. Place the folder `Pokemon5e` in `AppData/Local/FoundryVTT/Data/modules/` folder.

## Develop
### Requirements
Python 3.7 or higher as well as  
```
pip install requests
```


### Build
Run `python converter/main.py` and it will output the module content in `./dist*`

