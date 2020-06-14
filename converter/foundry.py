skill_name_to_abv = {
    "Acrobatics": "acr",
    "Animal Handling": "ani",
    "Arcana": "arc",
    "Athletics": "ath",
    "Deception": "dec",
    "History": "his",
    "Insight": "ins",
    "Intimidation": "itm",
    "Investigation": "inv",
    "Medicine": "med",
    "Nature": "nat",
    "Persuasion": "prc",
    "Performance": "prf",
    "Perception": "per",
    "Religion": "rel",
    "Sleight of Hand": "slt",
    "Stealth": "ste",
    "Survival": "sur"
}

skill_abv_to_name = {
     "acr": "Acrobatics",
     "ani": "Animal Handling",
     "arc": "Arcana",
     "ath": "Athletics",
     "dec": "Deception",
     "his": "History",
     "ins": "Insight",
     "itm": "Intimidation",
     "inv": "Investigation",
     "med": "Medicine",
     "nat": "Nature",
     "prc": "Persuasion",
     "prf": "Performance",
     "per": "Perception",
     "rel": "Religion",
     "slt": "Sleight of Hand",
     "ste": "Stealth",
     "sur": "Survival",
}

abilities = ["str", "dex", "con", "int", "wis", "cha"]

module_name = "Pokemon5e"
module_definition = {
    "name": module_name,
    "title": module_name,
    "description": "The Wonderful World of Pokémon - in Dungeons & Dragons 5E",
    "author": "Jerakin",
    "version": "0.1.0",
    "minimumCoreVersion": "0.5.0",
    "compatibleCoreVersion": "0.5.5",
    "packs": [
    ]
}


packs = {
    "pokemon": {
            "name": "features",
            "label": module_name,
            "path": "packs/p5e-pokemon.db",
            "entity": "Item",
            "module": module_name
        }
}
