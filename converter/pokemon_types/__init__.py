from converter.pokemon_types import _types

_type_map = {
    None: _types.BaseType(),
    "Normal": _types.Normal,
    "Fire": _types.Fire,
    "Water": _types.Water,
    "Electric": _types.Electric,
    "Grass": _types.Grass,
    "Ice": _types.Ice,
    "Fighting": _types.Fighting,
    "Poison": _types.Poison,
    "Ground": _types.Ground,
    "Flying": _types.Flying,
    "Psychic": _types.Psychic,
    "Bug": _types.Bug,
    "Rock": _types.Rock,
    "Ghost": _types.Ghost,
    "Dragon": _types.Dragon,
    "Dark": _types.Dark,
    "Steel": _types.Steel,
    "Fairy": _types.Fairy
}


def type_filter(f, weakness):
    result = []
    for t, value in weakness.items():
        if f(value):
            result.append(t)
    return result


class Model:
    def __init__(self, type_1, type_2=None):
        self.weaknesses = {}
        self.__calculate_sums(_type_map[type_1], _type_map[type_2])

        self.vulnerabilities = type_filter(lambda a: a > 1, self.weaknesses)
        self.immunities = type_filter(lambda a:a == 0, self.weaknesses)
        self.resistances = type_filter(lambda a: a < 1 and a > 0, self.weaknesses)

    def __calculate_sums(self, type1, type2):
        self.weaknesses["normal"] = type1.normal * type2.normal
        self.weaknesses["fire"] = type1.fire * type2.fire
        self.weaknesses["water"] = type1.water * type2.water
        self.weaknesses["electric"] = type1.electric * type2.electric
        self.weaknesses["grass"] = type1.grass * type2.grass
        self.weaknesses["ice"] = type1.ice * type2.ice
        self.weaknesses["fighting"] = type1.fighting * type2.fighting
        self.weaknesses["poison"] = type1.poison * type2.poison
        self.weaknesses["ground"] = type1.ground * type2.ground
        self.weaknesses["flying"] = type1.flying * type2.flying
        self.weaknesses["psychic"] = type1.psychic * type2.psychic
        self.weaknesses["bug"] = type1.bug * type2.bug
        self.weaknesses["rock"] = type1.rock * type2.rock
        self.weaknesses["ghost"] = type1.ghost * type2.ghost
        self.weaknesses["dragon"] = type1.dragon * type2.dragon
        self.weaknesses["dark"] = type1.dark * type2.dark
        self.weaknesses["steel"] = type1.steel * type2.steel
        self.weaknesses["fairy"] = type1.fairy * type2.fairy
